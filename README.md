## Run Locally

### Requirements

It is necessary to have PostgreSQL installed and then to enter to
the PostgreSQL interactive terminal program, execute:

```sh
$  psql postgres
```

Then execute the following commands:

```sh
# CREATE USER user_kilimo WITH PASSWORD 'kilimo';
# ALTER ROLE user_kilimo CREATEDB;
# CREATE DATABASE kilimo_db;
# GRANT ALL PRIVILEGES ON DATABASE kilimo_db TO user_kilimo;
```

### Clone repository

```sh
$  git clone https://github.com/eemanuel/kilimo_test
```

### Create virtualenv

Above the cloned directory

```sh
$  virtualenv venv
$  source venv/bin/activate
```

### Install requirements

At the same level than manage.py

```sh
$  pip install -r requirements/local.txt
```

### To run development server inside virtualenv

Make migrations and migrate:

```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

Create the unique user instance:

```sh
$ python manage.py createsuperuser
```

Here, you will enter your desired username and press enter key.
You will then be prompted for your desired email address:
The final step is to enter your password.

You can access to admin only with this superuser.

Then run the local server:

```sh
$ python manage.py runserver
```

### Check in browser the url

```sh
http://localhost:8000/
```

## Endpoints

**Create Field:**
field/create/

**Create Rain:**
rain/create/

**List:**
field/rain_avg_list/

**Detail:**
field/accomulated_rain_list/

**Update:**
field/<int:pk>/all_rain/

**Admin:**
admin/
