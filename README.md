The complete guide to running the code

## Installation and Set Up
Prerequisites:
* [Python 2](https://www.python.org/download/releases/2.7.2/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)
* MySQL


Clone the repo from GitHub:
```
git clone https://github.com/olawolemoses/features
```

Create a virtual environment for the project and activate it:
```
virtualenv venv
source venv/bin/activate
```

Install the required packages:
```
pip install --upgrade setuptools
pip install mysqlpy
pip install -r requirements.txt
```

## Database configuration
* Create a MySQL user your terminal and a MySQL database.
* Grant all privileges on your database to the user, like so:

```
$ mysql -uroot -p

mysql> CREATE USER 'iws_admin'@'localhost' IDENTIFIED BY 'iws2016';

mysql> CREATE DATABASE `hrequests-dev`;

mysql> GRANT ALL PRIVILEGES ON `hrequests-dev` . * TO 'iws_admin'@'localhost';
```

* `python manager.py db init`
* `python manager.py db migrate`
* `python manager.py db upgrade`
* `python manager.py deploy`

## instance/config.py file
In the directory `config.py` file currently exist. The app has the following configuration variables:
* SECRET_KEY
* SQLALCHEMY_DATABASE_URI (`'mysql://iws_admin:iws2016@localhost/hrequests-dev'`)

## Launching the Program
You can now run the app with the following command:

* `python manager.py runserver`

## Testing
First, create a test database and grant all privileges on your test database to your user:

```
$ mysql -u root

mysql> CREATE DATABASE `hrequests-test`;

mysql> GRANT ALL PRIVILEGES ON `hrequests-test` . * TO 'iws_admin'@'localhost';
```

To test, run the following command: `python manager.py test`

## Built With...
* [Flask](http://flask.pocoo.org/)

## Credits and License

Copyright (c) 2018 [olawolemoses](https://github.com/olawolemoses)
