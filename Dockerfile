FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install gunicorn==23.0.0
RUN pip install -r requirements.txt --no-cache-dir
