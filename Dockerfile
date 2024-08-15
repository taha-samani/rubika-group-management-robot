FROM python:3.12.3

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install build-essential -y

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "bot.py"]