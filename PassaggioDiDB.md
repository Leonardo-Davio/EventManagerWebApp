# Passaggio Db
- CMD > del all_data.json
- env > DB_ENGIN=postgres  
- CMD > python manage.py dumpdata > all_data.json
- env > DB_ENGIN=sqlite
- CMD > del db.sqlite3
- CMD > python manage.py migrate
- file> all_data.json **Cambia codifica**
- CMD > python manage.py loaddata all_data.json
