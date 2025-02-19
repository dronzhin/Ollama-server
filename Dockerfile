FROM ollama/ollama:latest

# Установка переменной окружения для отключения интерактивных запросов
ENV DEBIAN_FRONTEND=noninteractive

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3-pip \
    git \
    tzdata \
    && ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m pip install --upgrade pip

WORKDIR /app
COPY app /app
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Загрузка модели с предварительным запуском сервиса Ollama
RUN ollama serve > /dev/null 2>&1 & \
    sleep 10 && ollama pull llama3.2  # Используем корректное имя модели

EXPOSE 8005
CMD ["sh", "-c", "ollama serve > /dev/null 2>&1 & uvicorn main:app --host 0.0.0.0 --port 8005"]