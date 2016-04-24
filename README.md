![](harnas/home/static/logo.png)

# Harnaś

Harnaś (pol. kind of highlander) - system meant to be used by educational institutions, which focuses on automated checking of programming assigments. We want to provide easy to use, highly configurable environment, which can handle different technologies from C++ through SQL to CUDA.

## Technologies

- [Hera](https://github.com/zielmicha/hera) - sandbox used to protect against malicious users.
- [pandoc](http://pandoc.org/) - tool used to provide easy to use markup language (pandoc flavored markdown) and then converting it to html/pdf. You need to install it manually, probably from your distro repository.

## Setting up

Create virtual environment (for example using `virtualenv-wrapper`) and install dependencies:

```
mkvirtualenv -p /usr/bin/python3.4 venv
pip install -r requirements.txt
```

Copy settings and customize:

```
cp local_settings.py.example local_settings.py
```


Set up the database:

```
./manage.py migrate
```

Load initial data:

```
 ./manage.py loaddata initial-data.yaml
```

Create superuser:

```
./manage.py createsuperuser
```
