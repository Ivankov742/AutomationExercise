# Используем официальный образ Playwright с Python и браузерами
FROM mcr.microsoft.com/playwright/python:v1.54.0-jammy

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаем зависимости проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники
COPY . .

# Готовим каталоги отчётов (на всякий случай)
RUN mkdir -p reports/html reports/allure-results

# В контейнере всегда headless (как в CI)
ENV CI=true
# Можно при желании пробросить язык/локаль (не обязательно)
ENV PYTHONUNBUFFERED=1

# По умолчанию запускаем pytest; любые аргументы, переданные контейнеру,
# будут добавлены к pytest (например, "docker run image -m ui").
ENTRYPOINT ["pytest"]
CMD ["-q", "--tracing=retain-on-failure", "--video=retain-on-failure"]
