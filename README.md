How to install?
===============

```
$ git clone --recursive git@github.com:mahendrakalkura/mysql.git
$ cd mysql
$ mkvirtualenv --python=python3 mysql
$ pip install --requirement requirement.txt
```

How to run?
===========

```
$ cd mysql
$ python manage.py --host=... --port=... --user=... --password=... --database=...
$ python manage.py --host=... --port=... --user=... --password=... --database=... --table=...
```
