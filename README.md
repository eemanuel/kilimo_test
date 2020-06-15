## Kilimo Test

### Requirements

It is necessary to have PostgreSQL installed and then to enter to
the PostgreSQL interactive terminal program, execute:

```sh
$ psql postgres
```

Then execute the following commands:

```postgres
=# CREATE USER user_kilimo WITH PASSWORD 'kilimo';
=# ALTER ROLE user_kilimo CREATEDB;
=# CREATE DATABASE kilimo_db;
=# GRANT ALL PRIVILEGES ON DATABASE kilimo_db TO user_kilimo;
```

### Clone repository

```sh
$ git clone https://github.com/eemanuel/kilimo_test
```

### Create virtualenv

Above the cloned directory

```sh
$ virtualenv venv
$ source venv/bin/activate
```

### Install requirements

At the same level than manage.py

```sh
$ pip install -r requirements.txt
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

## Admin

```sh
http://localhost:8000/admin/
```

## Endpoints

**Create Field:**

[POST] /field/create/

**List Fields** (with their rain average at the last 'last_days' days)**:**

[GET] /field/rain_avg_list/?last_days=<int:last_days>

**List Fields** (when their accomulated rain is greather than 'accumulated_rain_gt')**:**

[GET] /field/accomulated_rain_list/?accumulated_rain_gt=<int:accumulated_rain_gt>

**List Rains** (form field)**:**

[GET] /field/<int:pk>/all_rain/

**Create Rain:**

[POST] /rain/create/
