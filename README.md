# Project Title

Django multiple user type.

## Description

We need django authentication which can handle multiple user types with different privileges

## Getting Started

### Executing program

run commands bellow to run project
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

### Notes

there are 3 types of user available

* superuser
    * the default superuser of django which can access admin panel
    * can crate supervisor
    * can access supervisor user signup view

* supervisor
    * can not access admin panel
    * can create normal user
    * can access normal user signup view

* normal
    * can not access admin panel
    * can not create any user
    * can not access any signup form

### Test

run command bellow to run unit tests
```
python3 manage.py test
```