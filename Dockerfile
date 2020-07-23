FROM python:3.6.9-alpine3.10

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]