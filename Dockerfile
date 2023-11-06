FROM python:latest

WORKDIR /apps

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5678

CMD ["python", "telegram_crawler.py"]
