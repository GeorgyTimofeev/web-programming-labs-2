from flask import Flask, url_for, redirect, abort, render_template, request
from werkzeug.exceptions import HTTPException
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

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
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
        <tytle>Ошибка 404</tytle>
    </head>
    <body>
        <h1>Упс… Кажется такой страницы не существует</h1>
        <p>Сервер не может найти запрошенный ресурс. В браузере это означает,
        что URL-адрес не распознан. В API это также может означать,
        что адрес правильный, но ресурс не существует.</p>

        <img src="''' + url_for('static', filename='Error_404_img.png') + '''" style="width: 300px;
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
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
        <tytle>Ошибка 500</tytle>
    </head>
    <body>
        <h1>Внутренняя ошибка сервера</h1>
        <p>На сервере произошла ошибка, в результате которой он не может успешно обработать запрос.
        Пожалуйста, попробуйте позже.</p>

        <img src="''' + url_for('static', filename='Error_500_img.png') + '''" style="width: 300px;
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
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</header>
        <ol>
            <li><a href="/lab1">Первая Лабораторная</a></li>
            <li><a href="/lab2">Вторая Лабораторная</a></li>
        </ol>
    </body>
    <footer>
        Тимофеев Георгий Алексеевич, ФБИ-22, 3 Курс, 2024 год.
    </footer>
</html>
'''


@app.route('/lab2/a')
def a_no_slash():
    return 'без слеша'

@app.route('/lab2/a/')
def a_slash():
    return 'со слешем'

flower_list = [
    {'name': 'Роза', 'price': 100},
    {'name': 'Лилия', 'price': 150},
    {'name': 'Тюльпан', 'price': 80},
    {'name': 'Орхидея', 'price': 200},
    {'name': 'Пион', 'price': 120},
    {'name': 'Астра', 'price': 90},
    {'name': 'Георгин', 'price': 110},
    {'name': 'Хризантема', 'price': 130},
    {'name': 'Гвоздика', 'price': 70},
    {'name': 'Ирис', 'price': 140}
]

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return render_template('flower_not_found.html'), 404
    else:
        flower = flower_list[flower_id]
        return render_template('flower.html', flower=flower)

@app.route('/lab2/request_flower/')
def request_flower():
    name = request.args.get('name')
    price = request.args.get('price')

    if not name or not price:
        return render_template("flower_error.html"), 400

    return redirect(url_for('add_flower', name=name, price=int(price)))

@app.route('/lab2/add_flower/', defaults={'name': None, 'price': None})
@app.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    if not name or price is None:
        return render_template("flower_error.html"), 400
    flower_list.append({'name': name, 'price': price})
    return render_template('flower_added.html', name=name, price=price, flower_list=flower_list)

@app.route('/lab2/all_flowers/')
def all_flowers():
    return render_template('all_flowers.html', flower_list=flower_list)

@app.route('/lab2/clear_flowers/')
def clear_flowers():
    global flower_list
    flower_list = []
    return render_template('flowers_cleared.html')

@app.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        return render_template('flower_not_found.html'), 404
    else:
        del flower_list[flower_id]
        return redirect(url_for('all_flowers'))

@app.route('/lab2/example/')
def example():
    name= "Тимофеев Георгий"
    lab_number = 2
    student_group = "ФБИ-22"
    student_course = 3
    fruits = [
        {'name': 'яблоко', 'price': 50},
        {'name': 'груша', 'price': 60},
        {'name': 'апельсин', 'price': 70},
        {'name': 'банан', 'price': 40},
        {'name': 'мандарин', 'price': 55}
    ]
    return render_template('example.html', name=name, lab_number=lab_number, student_group=student_group, student_course=student_course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters/')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/')
def calc_redirect():
    return redirect(url_for('calculate', num1=1, num2=1))

@app.route('/lab2/calc/<int:num1>/<int:num2>/')
def calculate(num1, num2):
    return render_template('calc.html', num1=num1, num2=num2)

@app.route('/lab2/calc/<int:num1>/')
def calc_redirect_with_num1(num1):
    return redirect(url_for('calculate', num1=num1, num2=1))

@app.route('/lab2/books/')
def books():
    books_list = [
        {'author': 'Джеймс Джойс', 'title': 'Улисс', 'genre': 'Роман', 'pages': 730},
        {'author': 'Джек Керуак', 'title': 'В дороге', 'genre': 'Роман', 'pages': 320},
        {'author': 'Федор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
        {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман', 'pages': 1225},
        {'author': 'Джордж Оруэлл', 'title': '1984', 'genre': 'Антиутопия', 'pages': 328},
        {'author': 'Габриэль Гарсиа Маркес', 'title': 'Сто лет одиночества', 'genre': 'Магический реализм', 'pages': 417},
        {'author': 'Фрэнсис Скотт Фицджеральд', 'title': 'Великий Гэтсби', 'genre': 'Роман', 'pages': 180},
        {'author': 'Харпер Ли', 'title': 'Убить пересмешника', 'genre': 'Роман', 'pages': 281},
        {'author': 'Дж. Р. Р. Толкин', 'title': 'Властелин колец', 'genre': 'Фэнтези', 'pages': 1178},
        {'author': 'Джейн Остин', 'title': 'Гордость и предубеждение', 'genre': 'Роман', 'pages': 279}
    ]
    return render_template('books.html', books=books_list)


@app.route('/lab2/mushrooms/')
def mushrooms_view():
    mushrooms = [
        {
            'name': 'Белый гриб',
            'description': 'Белый гриб, или боровик, — один из самых ценных и вкусных грибов.',
            'image': url_for('static', filename='mushroom_beliy.png')
        },
        {
            'name': 'Лисичка',
            'description': 'Лисички — съедобные грибы с ярко-оранжевыми шляпками и ножками.',
            'image': url_for('static', filename='mushroom_lisichka.png')
        },
        {
            'name': 'Подберезовик',
            'description': 'Подберезовик — съедобный гриб, который часто встречается в березовых лесах.',
            'image': url_for('static', filename='mushroom_podberezovik.png')
        },
        {
            'name': 'Опёнок',
            'description': 'Опёнок — съедобный гриб, который растет большими группами на пнях и деревьях.',
            'image': url_for('static', filename='mushroom_openok.png')
        },
        {
            'name': 'Шампиньон',
            'description': 'Шампиньон — один из самых популярных съедобных грибов, часто используемый в кулинарии.',
            'image': url_for('static', filename='mushroom_shampignon.png')
        }
    ]
    return render_template('mushrooms.html', mushrooms=mushrooms)
