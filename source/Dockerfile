FROM cgr.dev/chainguard/python:latest-dev as builder

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --user

ENTRYPOINT [ "python", "/app/app.py" ]
