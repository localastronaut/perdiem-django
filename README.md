# PerDiem
#### The world's first fan run record label

[![Build Status](https://travis-ci.org/RevolutionTech/perdiem-django.svg?branch=master)](https://travis-ci.org/RevolutionTech/perdiem-django)
[![codecov](https://codecov.io/gh/RevolutionTech/perdiem-django/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/perdiem-django)
[![Dependency Status](https://www.versioneye.com/user/projects/56db9ef4309a580033b7dd87/badge.svg?style=flat)](https://www.versioneye.com/user/projects/56db9ef4309a580033b7dd87)

## Setup

### Prerequisites

PerDiem requires [memcached](http://memcached.org/), [PostgreSQL](http://www.postgresql.org/), pip and libjpeg-dev, which you can install on debian with:

    $ sudo apt-get install memcached postgresql postgresql-contrib python-pip python-dev libpq-dev libjpeg-dev

I recommend using a virtual environment for PerDiem. If you don't have it already, you can install [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and virtualenvwrapper globally with pip:

    $ sudo pip install virtualenv virtualenvwrapper

[Update your .profile or .bashrc file](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file) to create new environment variables for virtualenvwrapper and then create and activate your virtual environment with:

    $ mkvirtualenv perdiem

In the future you can reactivate the virtual environment with:

    $ workon perdiem

### Installation

Then in your virtual environment, you will need to install Python dependencies such as [Gunicorn](http://gunicorn.org/), [django](https://www.djangoproject.com/), python-memcached, psycopg2, [pillow](https://pillow.readthedocs.org/), django-classbasedsettings, django-templated-email, [geopy](http://geopy.readthedocs.org/), and [Pinax Stripe](https://pinax-stripe.readthedocs.org/). You can do this simply with the command:

    $ pip install -r requirements.txt

### Configuration

Next we will need to create a file in the settings directory called `dev.py`. This is where we will store all of the settings that are specific to your instance of PerDiem. Most of these settings should be only known to you. Your file should subclass BaseSettings from `base.py` and then define a secret key and the database credentials. You will also need to define your development keys and secrets from Google, Facebook, Stripe, and MailChimp. Your `dev.py` file might look something like:

    from perdiem.settings.base import BaseSettings

    class DevSettings(BaseSettings):
        SECRET_KEY = '-3f5yh&(s5%9uigtx^yn=t_woj0@90__fr!t2b*96f5xoyzb%b'
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'perdiem',
                'USER': 'postgres',
                'PASSWORD': 'abc123',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
        SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1234-abc123.apps.googleusercontent.com'
        SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'abc123'
        SOCIAL_AUTH_FACEBOOK_KEY = '1234'
        SOCIAL_AUTH_FACEBOOK_SECRET = 'abc123'
        PINAX_STRIPE_PUBLIC_KEY = 'pk_test_abc123'
        PINAX_STRIPE_SECRET_KEY = 'sk_test_abc123'
        MAILCHIMP_API_KEY = 'abc123-usX'
        MAILCHIMP_LIST_ID = '1234'

Of course you should [generate your own secret key](http://stackoverflow.com/a/16630719) and use a more secure password for your database. If you like, you can override more of Django settings here. If you do not create this file, you will get a `cbsettings.exceptions.NoMatchingSettings` exception when starting the server.

With everything installed and all files in place, you may now create the database tables and collect static files. You can do this with:

    $ python manage.py migrate
    $ python manage.py collectstatic

### Deployment

In the production environment, you'll need to create a different dev settings configuration file. It will be similar to the one above, except that you will be using production keys and secrets instead of development keys. In addition, you will need to create a `prod.py` file, similar to your `dev.py` file, but this one will contain settings only relevant to production. This file is a good place to put keys and secrets for services that are only used in the production environment, such as Sentry. It may be best to subclass the `DevSettings` class you created, in order to get something like this:

    from perdiem.settings.dev import DevSettings

    class ProdSettings(DevSettings):
        DEBUG = False
        ALLOWED_HOSTS = ['127.0.0.1', 'localhost',]
        RAVEN_PUBLIC_KEY = 'xyz'
        RAVEN_SECRET_KEY = 'abc123'
        RAVEN_PROJECT_ID = '1234'
        DEFAULT_FILE_STORAGE = 'perdiem.custom_storages.MediaStorage'
        STATICFILES_STORAGE = 'perdiem.custom_storages.StaticStorage'
        AWS_STORAGE_BUCKET_NAME = 'perdiem-xyz'
        AWS_S3_CUSTOM_URL = 'https://{bucket}.s3.amazonaws.com'.format(bucket=AWS_STORAGE_BUCKET_NAME)
        AWS_ACCESS_KEY_ID = '1234'
        AWS_SECRET_ACCESS_KEY = 'abc123'
        AWS_SES_ACCESS_KEY_ID = '1234'
        AWS_SES_SECRET_ACCESS_KEY = 'abc123'
        EMAIL_BACKEND = 'django_ses.SESBackend'

For reference, the format of the Sentry DSN is as follows:

     {PROTOCOL}://{PUBLIC_KEY}:{SECRET_KEY}@{HOST}/{PATH}{PROJECT_ID}

Alternatively, you may choose to merge your production `dev.py` file into `prod.py`. In that case, be sure to subclass `BaseSettings` instead of `DevSettings` and make sure all definitions from `dev.py` are in `prod.py`.

PerDiem uses Gunicorn with [runit](http://smarden.org/runit/) and [Nginx](http://nginx.org/). You can install them with the following:

    $ sudo apt-get install runit nginx

The rest of the README assumes that the PerDiem repo was checked out in `/home/perdiem/`. Please replace this path as necessary.

We need to copy the Nginx configuration:

    $ cd /etc/nginx/sites-enabled
    $ sudo ln -s /home/perdiem/perdiem-django/perdiem/perdiem/nginx/investperdiem.com investperdiem.com

Then we need to create a script to run PerDiem on boot with runit:

    $ sudo mkdir /etc/sv/perdiem
    $ cd /etc/sv/perdiem
    $ sudo nano run

In this file, create a script similar to the following:

    #!/bin/sh

    GUNICORN=/home/perdiem/.virtualenvs/perdiem/bin/gunicorn
    ROOT=/home/perdiem/perdiem-django/perdiem
    PID=/var/run/gunicorn.pid

    APP=perdiem.wsgi:application

    if [ -f $PID ]; then rm $PID; fi

    cd $ROOT
    exec $GUNICORN -c $ROOT/perdiem/gunicorn.py --pid=$PID $APP

Then change the permissions on the file to be executable and symlink the project to /etc/service:

    $ sudo chmod u+x run
    $ sudo ln -s /etc/sv/perdiem /etc/service/perdiem

PerDiem should now automatically be running on the local machine.
