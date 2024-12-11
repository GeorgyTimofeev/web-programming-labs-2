from flask import Flask, url_for, redirect, abort, render_template, request, session
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy
from db import db
import os
from os import path
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'very-secret-key')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')


if app.config['DB_TYPE'] == 'postgres':
    db_name = "georgy_timofeev_orm"
    db_user = "georgy_timofeev_orm"
    db_password = "postgres"
    host_ip = "127.0.0.1"
    host_port = "5432"

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(os.path.realpath(__file__))
    db_path = path.join(dir_path, 'db.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

@app.errorhandler(400)
def bad_request(err):
    return '''Ошибка 400.
    Неверный запрос. Сервер не может или не будет обрабатывать запрос из-за чего-то,
    что воспринимается как ошибка клиента (например, неправильный синтаксис, формат
    или маршрутизация запроса).''', 400



@app.errorhandler(401)
def unauthorized(err):
    return '''Ошибка 401. Для доступа к ресурсу требуется аутентификация.
    Клиент должен передать заголовок Authorization в запросе.''', 401


class PaymentRequired(HTTPException):
    code = 402
    description = 'Payment Required'

@app.errorhandler(PaymentRequired)
def payment_required(err):
    return '''Ошибка 402. Зарезервировано для будущего использования.
    Используется для целей тестирования оплаты.''', 402



@app.errorhandler(403)
def forbidden(err):
    return '''Ошибка 403. Клиент не имеет прав доступа к содержимому,
    поэтому сервер отказывает в выполнении запроса.''', 403



@app.errorhandler(404)
def not_found(err):
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
        <tytle>Ошибка 404</tytle>
    </head>
    <body>
        <h1>Упс… Кажется такой страницы не существует</h1>
        <p>Сервер не может найти запрошенный ресурс. В браузере это означает,
        что URL-адрес не распознан. В API это также может означать,
        что адрес правильный, но ресурс не существует.</p>

        <img src="''' + url_for('static', filename='lab1/Error_404_img.png') + '''" style="width: 300px;
        position: absolute; top: 60%; right: 50px; transform: translateY(-50%);"></br>

        <a href="/">Вернуться на главную</a>
    </body>
''', 404



@app.errorhandler(405)
def method_not_allowed(err):
    return '''Ошибка 405. Метод, указанный в запросе (например, POST, PUT, DELETE) не применим к ресурсу,
    и сервер не поддерживает его.''', 405



@app.errorhandler(418)
def i_am_a_teapot(err):
    return '''Ошибка 418. Я… я – чай? Определенный в RFC 2324. Этот код составляет часть
    апрельской шутки и не должен использоваться для серьезных целей.''', 418



@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
        <tytle>Ошибка 500</tytle>
    </head>
    <body>
        <h1>Внутренняя ошибка сервера</h1>
        <p>На сервере произошла ошибка, в результате которой он не может успешно обработать запрос.
        Пожалуйста, попробуйте позже.</p>

        <img src="''' + url_for('static', filename='lab1/Error_500_img.png') + '''" style="width: 300px;
        position: absolute; top: 50%; right: 100px; transform: translateY(-50%);"></br>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 500



@app.route('/')
@app.route('/index')
def index():
    return '''
<!doctype html>
<html>
    <head>
        <tytle>НГТУ, ФБ, Лабораторные работы</tytle>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
    </head>
    <body>
        <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</header>
        <ol>
            <li><a href="/lab1">Первая Лабораторная</a></li>
            <li><a href="/lab2">Вторая Лабораторная</a></li>
            <li><a href="/lab3">Третья Лабораторная</a></li>
            <li><a href="/lab4">Четвертая Лабораторная</a></li>
            <li><a href="/lab5">Пятая Лабораторная</a></li>
            <li><a href="/lab6">Шестая Лабораторная</a></li>
            <li><a href="/lab7">Седьмая Лабораторная</a></li>
            <li><a href="/lab8">Восьмая Лабораторная</a></li>
        </ol>
    </body>
    <footer>
        Тимофеев Георгий Алексеевич, ФБИ-22, 3 Курс, 2024 год.
    </footer>
</html>
'''
