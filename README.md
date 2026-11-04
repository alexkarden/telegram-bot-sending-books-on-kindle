# Telegram Bot for Sending Books to Kindle

Telegram-бот, который принимает электронные книги в чате и отправляет их
на устройство **Amazon Kindle** по email.

Пользователь отправляет файл книги боту, указывает email Kindle-устройства,
а бот пересылает файл через SMTP. Поддерживается запуск в Docker.

## Возможности

- Приём электронных книг в Telegram
- Отправка файлов на Kindle через email
- Сохранение email Kindle-устройства в базе данных
- Повторная отправка книги без повторного ввода адреса
- Асинхронная работа Telegram-бота
- Запуск через Docker Compose

## Как работает

```text
Пользователь
     │
     ▼
Telegram Bot (aiogram)
     │
     ├──▶ SQLite: email Kindle и настройки пользователя
     │
     ▼
SMTP / Amazon Kindle email
     │
     ▼
Kindle
```

1. Пользователь отправляет боту файл книги.
2. Бот проверяет формат и размер файла.
3. Пользователь указывает email своего Kindle, если он ещё не сохранён.
4. Бот отправляет файл на Kindle через SMTP.
5. Amazon доставляет книгу на устройство.

## Поддерживаемые форматы

Обычно Kindle принимает документы и книги в форматах:

- `.mobi`
- `.pdf`
- `.doc`
- `.docx`
- `.txt`
- `.rtf`
- `.html`

Перед использованием проверьте актуальные ограничения Amazon для
Send-to-Kindle: допустимые форматы, максимальный размер вложения и количество
файлов в письме.

## Технологии

| Компонент | Технология |
|---|---|
| Telegram Bot | aiogram 3 |
| Язык | Python 3 |
| База данных | SQLite |
| Отправка на Kindle | SMTP |
| Контейнеризация | Docker, Docker Compose |

## Быстрый старт

### Локальный запуск

```bash
git clone [https://github.com/alexkarden/telegram-bot-sending-books-on-kindle.git](https://github.com/alexkarden/telegram-bot-sending-books-on-kindle.git)
cd telegram-bot-sending-books-on-kindle

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
```

Заполните `.env`:

```env
BOT_TOKEN=your_telegram_bot_token
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SENDER_EMAIL=your_email@gmail.com
DATABASE_PATH=bot.db
```

Запуск:

```bash
python run.py
```

### Запуск через Docker

```bash
cp .env.example .env
docker compose up -d --build
```

## Настройка Kindle

1. В Amazon аккаунте откройте раздел **Manage Your Content and Devices**.
2. Перейдите в **Preferences → Personal Document Settings**.
3. Добавьте email, с которого бот отправляет книги, в список разрешённых отправителей.
4. Скопируйте email вашего Kindle в формате `your_name@kindle.com`.
5. Отправьте этот email боту при первом использовании.

## Команды бота

| Команда | Описание |
|---|---|
| `/start` | Регистрация и главное меню |
| `/kindle` | Указать или изменить email Kindle |
| `/help` | Справка по использованию |

## Пример работы

```text
Пользователь: отправляет book.epub

Бот: 📚 Файл получен.
Укажите email вашего Kindle:

Пользователь: my_kindle@kindle.com

Бот: ✅ Книга отправлена на your Kindle.
```

## Безопасность

- Не публикуйте `BOT_TOKEN`, пароль SMTP или пароль приложения в коде.
- Используйте `.env` и добавьте его в `.gitignore`.
- Для Gmail создайте **App Password**, а не используйте основной пароль аккаунта.
- Разрешите в Amazon только email, с которого бот отправляет книги.

## Структура проекта

```text
.
├── handlers.py       # Обработчики Telegram-сообщений и файлов
├── keyboards.py      # Клавиатуры бота
├── emailscript.py    # Отправка книги на Kindle через SMTP
├── database.py       # Работа с SQLite
├── run.py            # Точка входа
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Лицензия

MIT
