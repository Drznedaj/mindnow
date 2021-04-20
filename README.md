# mindnow

HolyCode / Mindnow backend task in Python 3.6 using Django framework

If running with Docker GeoIP2 city and country databases have to be put
in the geoip directory in the root of this project.

Run with:
```bash
docker-compose up
```

I suggest making a virtual environment for Python dependencies if not runing with docker.

For email verification of users to work run in another console:
```bash
python -m smtpd -n -c DebuggingServer localhost:1025
```

Otherwise just run with:
```bash
python manage.py runserver
```
