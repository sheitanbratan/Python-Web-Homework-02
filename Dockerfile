FROM python:3.11

LABEL maintainer='https://github.com/sheitanbratan'

WORKDIR /app

COPY . .

ENTRYPOINT [ "python", "src/main.py" ]