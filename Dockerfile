FROM python:3.9.24-slim-trixie
WORKDIR /app
COPY . /app

RUN apt update -y && apt install awscli -y

RUN apt-get update && pip install -r requirements.txt
CMD ["python3", "app.py"]