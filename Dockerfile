FROM python:3.12-slim

WORKDIR /app

ENV PORT=8082

COPY . /app

CMD [ "python3", "server.py" ]

