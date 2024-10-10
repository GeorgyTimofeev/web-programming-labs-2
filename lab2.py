from flask import Blueprint, url_for, redirect, abort, render_template, request
from werkzeug.exceptions import HTTPException
lab2 = Blueprint('lab2',__name__)

@lab2.route('/lab2/a')
def a_no_slash():
    return 'без слеша'

@lab2.route('/lab2/a/')
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

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return render_template('flower_not_found.html'), 404
    else:
        flower = flower_list[flower_id]
        return render_template('flower.html', flower=flower)

@lab2.route('/lab2/request_flower/')
def request_flower():
    name = request.args.get('name')
    price = request.args.get('price')

    if not name or not price:
        return render_template("flower_error.html"), 400

    return redirect(url_for('lab2.add_flower', name=name, price=int(price)))

@lab2.route('/lab2/add_flower/', defaults={'name': None, 'price': None})
@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    if not name or price is None:
        return render_template("flower_error.html"), 400
    flower_list.append({'name': name, 'price': price})
    return render_template('flower_added.html', name=name, price=price, flower_list=flower_list)

@lab2.route('/lab2/all_flowers/')
def all_flowers():
    return render_template('all_flowers.html', flower_list=flower_list)

@lab2.route('/lab2/clear_flowers/')
def clear_flowers():
    global flower_list
    flower_list = []
    return render_template('flowers_cleared.html')

@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        return render_template('flower_not_found.html'), 404
    else:
        del flower_list[flower_id]
        return redirect(url_for('lab2.all_flowers'))

@lab2.route('/lab2/example/')
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

@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')

@lab2.route('/lab2/filters/')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@lab2.route('/lab2/calc/')
def calc_redirect():
    return redirect(url_for('lab2.calculate', num1=1, num2=1))

@lab2.route('/lab2/calc/<int:num1>/<int:num2>/')
def calculate(num1, num2):
    return render_template('calc.html', num1=num1, num2=num2)

@lab2.route('/lab2/calc/<int:num1>/')
def calc_redirect_with_num1(num1):
    return redirect(url_for('lab2.calculate', num1=num1, num2=1))

@lab2.route('/lab2/books/')
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


@lab2.route('/lab2/mushrooms/')
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
