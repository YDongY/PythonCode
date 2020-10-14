# Flask Project Demo 


[![Flask Web Development, 2nd Edition](https://images-na.ssl-images-amazon.com/images/I/51djSJpTN5L._SX379_BO1,204,203,200_.jpg)](http://flaskbook.com/)

Flask Web 开发　是一本非常好的书，学习 Flask 必备书籍，本项目只是把书中项目的组织框架留着，具体内容代码可查看下方连接。

> 原作者代码：[https://github.com/miguelgrinberg/flasky](https://github.com/miguelgrinberg/flasky)

```
$ tree
.
├── app
│   ├── api
│   │   └── __init__.py
│   ├── auth
│   │   └── __init__.py
│   ├── email.py
│   ├── __init__.py
│   ├── main
│   │   ├── errors.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── views.py
│   ├── models.py
│   ├── static
│   └── templates
├── config.py
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
├── requirements.txt
└── tests
    ├── __init__.py
    └── test_basics.py
```

## 安装

```shell script
pip install -r requirements.txt
```

## 运行

```shell script
$ python manage.py
usage: manage.py [-?] {test,shell,db,show-urls,clean,runserver} ...

positional arguments:
  {test,shell,db,show-urls,clean,runserver}
    test
    shell               Runs a Python shell inside Flask application context.
    db                  Perform database migrations
    show-urls           Displays all of the url matching routes for the
                        project
    clean               Remove *.pyc and *.pyo files recursively starting at
                        current directory
    runserver           Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help            show this help message and exit
```


```shell script
$ export FLASK_APP=flasky.py
$ flask       
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  Provides commands from Flask, extensions, and the application. Loads the
  application defined in the FLASK_APP environment variable, or from a
  wsgi.py file. Setting the FLASK_ENV environment variable to 'development'
  will enable debug mode.

    $ export FLASK_APP=hello.py
    $ export FLASK_ENV=development
    $ flask run

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  db      Perform database migrations.
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
  test
```
