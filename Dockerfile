# Указываем базовый образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем оставшиеся файлы в контейнер
COPY . .

# Запускаем приложение
CMD ["python", "run.py"]  # Замените на точку входа вашего приложения