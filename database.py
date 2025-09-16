import logging
import os
import time

import aiosqlite
from dotenv import load_dotenv


load_dotenv()
DATABASE_NAME = os.getenv("DB_NAME")


# Инициализация базы данных
async def init_db():
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            # Создание таблицы users, если она еще не существует
            await db.execute(
                ""
                "CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id INTEGER UNIQUE, "
                "first_name TEXT, "
                "last_name TEXT, "
                "username TEXT, "
                "user_added INTEGER NOT NULL, "
                "user_blocked INTEGER NOT NULL, "
                "type_of_notification TEXT, "
                "notification_frequency TEXT,"
                "created_at INTEGER,"
                "kindle_email TEXT)"
                ""
            )
            await db.commit()
    except aiosqlite.Error as e:
        logging.error(f"Ошибка при инициализации базы данных: {e}")


# Добавляем нового пользователя
async def add_user_db(user_id, first_name, last_name, username):
    created_at = int(time.time())
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            # Проверка, существует ли пользователь в базе данных
            async with db.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                result = await cursor.fetchone()
                if result is not None:
                    # Если пользователь существует, можно обновить его данные
                    await db.execute(
                        "UPDATE users SET first_name = ?, "
                        "last_name = ?, "
                        "username = ?, "
                        "user_added = ? WHERE user_id = ? ",
                        (first_name, last_name, username, 1, user_id),
                    )
                    logging.info(f"Пользователь с ID {user_id} обновлен в базе данных.")
                else:
                    # Если не существует, добавляем нового пользователя
                    await db.execute(
                        "INSERT INTO users ("
                        "user_id, "
                        "first_name, "
                        "last_name, "
                        "username, "
                        "user_added, "
                        "user_blocked, "
                        "created_at, "
                        "type_of_notification, "
                        "notification_frequency ) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)",
                        (
                            user_id,
                            first_name,
                            last_name,
                            username,
                            1,
                            0,
                            created_at,
                            "full",
                            "never",
                        ),
                    )
                    logging.info(f"Пользователь с ID {user_id} добавлен в базу данных.")
                await db.commit()
    except aiosqlite.Error as e:
        logging.error(f"Ошибка при добавлении пользователя в базу данных: {e}")
    except Exception as e:
        logging.error(f"Произошла неожиданная ошибка: {e}")


# проверяем есть ли почта у пользователя
async def get_user_email_from_db(user_id):
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            # Проверка, существует ли пользователь в базе данных
            async with db.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                result = await cursor.fetchone()
                if result:
                    return result[10]
                else:
                    return None

    except aiosqlite.Error as e:
        logging.error(f"Ошибка при получении почты пользователя из базы: {e}")
    except Exception as e:
        logging.error(f"Произошла неожиданная ошибка: {e}")


# Добавляем новый email
async def add_user_email(user_id, useremail):
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            await db.execute(
                "UPDATE users SET kindle_email = ? WHERE user_id = ? ",
                (useremail, user_id),
            )
            await db.commit()
    except aiosqlite.Error as e:
        logging.error(f"Ошибка при добавлении email пользователя в базу данных: {e}")
    except Exception as e:
        logging.error(f"Произошла неожиданная ошибка: {e}")
