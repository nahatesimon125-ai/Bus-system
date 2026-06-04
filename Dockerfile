FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# copy project
COPY . /app

# install python deps
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# expose a default port (container will respect runtime PORT env)
EXPOSE 3000

# At container start: run migrations and collectstatic, then start gunicorn bound to $PORT (default 3000)
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput || true && exec gunicorn nts_project.wsgi:application --bind 0.0.0.0:${PORT:-3000} --workers 2"]
