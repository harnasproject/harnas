![](harnas/home/static/logo.png)

# Harnaś

Harnaś (pol. kind of highlander) - system meant to be used by educational institutions, which focuses on automated checking of programming assigments. We want to provide easy to use, highly configurable environment, which can handle different technologies from C++ through SQL to CUDA.

## Technologies

- [Hera](https://github.com/zielmicha/hera) - sandbox used to protect against malicious users.
- [pandoc](http://pandoc.org/) - tool used to provide easy to use markup language (pandoc flavored markdown) and then converting it to html/pdf. You need to install it manually, probably from your distro repository.

## Setting up

It is convenient to use Vagrant box as a development environment for Harnaś. Provisioning script is provided to ease the process of setting things up, so you only need to execute:

```
vagrant up
```

in root directory of the project. By default it will mount root directory as a shared folder to `/vagrant` and forward port `8000`. After the box is up, you need to execute some commands by hand, firstly create virtual environment (for example using `virtualenv-wrapper`) and install dependencies:

```
mkvirtualenv -p /usr/bin/python3.4 harnas
cd /vagrant
pip install -r requirements.txt
```

Then you need to copy local settings defaults and customize them (description is provided inside the example file):

```
cp local_settings.py.example local_settings.py
```

Finally you need to set up database and feed it with initial data:

```
./manage.py migrate
./manage.py loaddata initial-data.yaml
```

You will also probably need a superuser:

```
./manage.py createsuperuser
```
