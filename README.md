The complete guide to running the code

## Installation and Set Up
Prerequisites:
* [Python 2](https://www.python.org/download/releases/2.7.2/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)

Clone the repo from GitHub:
```
git clone https://github.com/olawolemoses/features
```

Create a virtual environment for the project and activate it:
```
virtualenv venv
source features/bin/activate
```

Install the required packages:
```
pip install -r requirements.txt
```

## Database configuration
* Create a MySQL user your terminal and a MySQL database.
* Grant all privileges on your database to the user, like so:

```
$ mysql -u root

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
* SQLALCHEMY_DATABASE_URI (`'mysql://iws_admin:iws2016@localhost/hrequests'`)

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

Copyright (c) 2017 [Mbithe Nzomo](https://github.com/olawolemoses)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
