# nishauri application

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/palladiumkenya/nishauri_api
$ cd nishauri_api
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd Nishauri_API
```

Update database crentials save and run migrations:
```
(env)$ nano settings
(env)$ cd ..
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```

Run the server:
```
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/api .

ALL SET.

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test
```
