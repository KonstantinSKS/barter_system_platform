FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install gunicorn==23.0.0 && \
    pip install -r requirements.txt --no-cache-dir

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120", "--chdir=/app"]
