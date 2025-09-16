import mimetypes
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path


def send_document_via_gmail(
    sender_email: str,
    app_password: str,
    to_email: str,
    subject: str,
    body: str,
    attachment_path: str,
) -> None:
    """
    Отправляет письмо с прикреплённым файлом через SMTP Gmail.
    sender_email: ваш Gmail (например, example@gmail.com)
    app_password: app password или обычный пароль (рекомендуется app password)
    to_email: получатель
    attachment_path: путь к файлу для прикрепления
    """
    # Подготовка сообщения
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Прикрепляем файл
    path = Path(attachment_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {attachment_path}")

    # Определяем MIME тип
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type is None:
        maintype, subtype = "application", "octet-stream"
    else:
        maintype, subtype = mime_type.split("/", 1)

    with path.open("rb") as f:
        file_data = f.read()
        file_name = path.name
        msg.add_attachment(
            file_data, maintype=maintype, subtype=subtype, filename=file_name
        )

    # Отправка через SMTP SSL
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL порт

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)
