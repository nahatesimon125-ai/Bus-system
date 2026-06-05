# NTS Regional Bus Tickets Uganda

A Django web application for regional bus trip browsing, seat booking, ticket history, and staff operations.

## Local setup

Use Python 3.13 to match the recommended PythonAnywhere deployment target.

```bash
py -3.13 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py test
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Default demo accounts

Customer:

```text
email: customer@nts.ug
password: password
```

Staff:

```text
email: admin@nts.ug
password: admin
```

## Environment variables

Copy `.env.example` values into your PythonAnywhere Web tab environment variables, or export them before running the app.

```text
DJANGO_SECRET_KEY=replace-this-with-a-long-random-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_SECURE_HSTS_SECONDS=31536000
```

For local development, leaving these unset is fine.

## PythonAnywhere files

Use `pythonanywhere_wsgi.py` as the reference for the PythonAnywhere WSGI configuration. Replace `yourusername` in the deployment commands and environment variables with your actual PythonAnywhere username.
