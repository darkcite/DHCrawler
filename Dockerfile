FROM python:latest

WORKDIR /app

# You can set default values for your environment variables here if you like
# ENV TELEGRAM_API_ID=default_value
# ENV TELEGRAM_API_HASH=default_value

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5678

CMD ["python", "telegram_crawler.py"]
