FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
COPY .env.example /app/.env.example
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 CMD curl --fail http://localhost:5000/ || exit 1
CMD ["flask", "run", "--host=0.0.0.0"]