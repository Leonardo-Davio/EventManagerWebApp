web: gunicorn EventManagerWebApp.wsgi --log-file -
web: python manage.py migrate && gunicorn EventManagerWebApp.wsgi