import logging
import os
from pathlib import Path
from uuid import uuid4

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from database import add_user_db, add_user_email, get_user_email_from_db
from emailscript import send_document_via_gmail
from keyboards import main_keyboard
from script import delete_file, is_email_simple, sanitize_filename


load_dotenv()
router = Router()

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = (25 * 1024 * 1024) - 1  # 25 MB


@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "👋 <b>Добро пожаловать!</b>\n\n"
        "📚 Просто отправьте файл книги в бот, "
        "и он отправит книгу на ваш <b>Kindle</b>.\n\n"
        "📧 Чтобы посмотреть ваш E‑mail, введите команду <code>/myemail</code> "
        "или нажмите кнопку — <b>Моя почта Kindle</b>.\n\n"
        "✏️ Чтобы изменить E‑mail, просто отправьте новый адрес боту "
        "(принимаются только адреса в домене kindle.com)."
    )

    # Записываем пользователя в базу
    await add_user_db(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username,
    )
    await message.answer(
        welcome_text, reply_markup=main_keyboard, parse_mode=ParseMode.HTML
    )
    emailbool = await get_user_email_from_db(message.from_user.id)
    if emailbool:
        await message.answer(
            f"{emailbool} - Ваша почта, на которую бот будет отправлять книги",
            reply_markup=main_keyboard,
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.answer(
            "Вы еще не отправили боту Ваш E-mail Kindle - отправка книг невозможна",
            reply_markup=main_keyboard,
            parse_mode=ParseMode.HTML,
        )


# Обрабатываем исключительно текстовые сообщения (чтобы не перехватывать документы/фото)
@router.message(F.content_type == types.ContentType.TEXT)
async def all_message(message: Message):
    text = str(message.text)
    if text == "Моя почта Kindle" or text == "/myemail":
        emailbool = await get_user_email_from_db(message.from_user.id)
        if emailbool:
            await message.answer(
                f"{emailbool} - Ваша почта, на которую бот будет отправлять книги",
                reply_markup=main_keyboard,
                parse_mode=ParseMode.HTML,
            )
        else:
            await message.answer(
                "Вы еще не отправили боту Ваш E-mail Kindle - отправка книг невозможна",
                reply_markup=main_keyboard,
                parse_mode=ParseMode.HTML,
            )

    else:
        if is_email_simple(text):
            await add_user_email(message.from_user.id, text)
            await message.answer(
                f"Почта {text} добавлена",
                reply_markup=main_keyboard,
                parse_mode=ParseMode.HTML,
            )
        else:
            await message.answer(
                "Бот принимает только файлы и адреса E-mail в доменной зоне kindle.com",
                reply_markup=main_keyboard,
                parse_mode=ParseMode.HTML,
            )


@router.message(F.content_type == types.ContentType.DOCUMENT)
async def handle_document(message: Message):
    doc = message.document
    if doc is None:
        return

    if doc.file_size is not None and doc.file_size > MAX_FILE_SIZE:
        await message.reply("Файл слишком большой. Лимит 25 MB.")
        logging.warning(
            "Пользователь %s прислал слишком большой документ: %s bytes",
            message.from_user.id,
            doc.file_size,
        )
        return

    orig_name = doc.file_name or f"{doc.file_unique_id}.bin"
    safe_name = sanitize_filename(orig_name)
    dest_name = f"{uuid4().hex}_{safe_name}"
    dest_path = DOWNLOAD_DIR / dest_name
    try:
        file = await message.bot.get_file(doc.file_id)  # возвращает types.File
        await message.bot.download_file(file.file_path, destination=dest_path)
        logging.info(
            "Сохранен документ пользователя %s: %s -> %s",
            message.from_user.id,
            orig_name,
            dest_path,
        )
        emailbool = await get_user_email_from_db(message.from_user.id)
        if emailbool:
            sender_email = os.getenv("SENDER_EMAIL")
            app_password = os.getenv("APP_PASSWORD")
            to_email = emailbool
            subject = os.getenv("SUBJECT")
            body = os.getenv("BODY")
            attachment_path = dest_path

            send_document_via_gmail(
                sender_email, app_password, to_email, subject, body, attachment_path
            )
            delete_file(dest_path)
            await message.answer(
                "Книга отправлена на Ваш Kindle",
                reply_markup=main_keyboard,
                parse_mode=ParseMode.HTML,
            )
        else:
            await message.answer(
                "Вы еще не отправили боту Ваш E-mail Kindle - отправка книг невозможна",
                reply_markup=main_keyboard,
                parse_mode=ParseMode.HTML,
            )

    except Exception as e:
        logging.exception(
            "Ошибка при сохранении документа от %s: %s", message.from_user.id, e
        )
        await message.reply("Ошибка при сохранении файла. Попробуйте ещё раз.")
