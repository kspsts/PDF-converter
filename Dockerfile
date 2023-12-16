FROM python:3.12

COPY . /app/
WORKDIR /app

RUN apt-get update && \
    apt-get install -y poppler-utils && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y tesseract-ocr-rus && \
    apt-get install tesseract-ocr-eng && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
