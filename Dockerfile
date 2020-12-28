FROM python:3.8

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
COPY entrypoint.sh /app/entrypoint.sh

WORKDIR /app

CMD ["./entrypoint.sh"]