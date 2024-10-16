from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response
lab3 = Blueprint('lab3',__name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    user = request.cookies.get('user')
    return render_template('lab3/lab3.html', user=user, name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie/')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookies/')
def del_cookies():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    resp.delete_cookie('user')
    return resp

@lab3.route('/lab3/form1/')
def form1():
    errors = {}

    user = request.args.get('user')

    if user == '':
        errors['user'] = 'Введите имя'

    age = request.args.get('age')

    if age == '':
        errors['age'] = 'Введите возраст'


    sex = request.args.get('sex')

    if sex == '':
        errors['sex'] = 'Введите свой пол'

    if request.args.get('clear'):
        resp = make_response(redirect(url_for('lab3.form1')))
        resp.set_cookie('user', '', expires=0)
        resp.set_cookie('age', '', expires=0)
        resp.set_cookie('sex', '', expires=0)
        return resp

    if user or age or sex:
        resp = make_response(render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors))
        if user:
            resp.set_cookie('user', user)
        if age:
            resp.set_cookie('age', age)
        if sex:
            resp.set_cookie('sex', sex)
        return resp

    user = request.cookies.get('user')
    age = request.cookies.get('age')
    sex = request.cookies.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order/')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/payment/')
def payment():
    price = 0
    drink = request.args.get('drink')

    if drink == 'coffee':
        price += 120
    elif drink == 'black_tea':
        price += 80
    elif drink == 'green_tea':
        price += 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/payment.html', price=price)

@lab3.route('/lab3/success/', methods=['GET', 'POST'])
def success():
    if request.method == 'POST':
        price = request.form.get('price')
        return render_template('lab3/success.html', price=price)
    else:
        return redirect(url_for('lab3.order'))

@lab3.route('/lab3/settings/', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        color = request.form.get('color')
        bg_color = request.form.get('bg_color')
        font_size = request.form.get('font_size')
        font_weight = request.form.get('font_weight')

        resp = make_response(redirect(url_for('lab3.settings')))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_weight:
            resp.set_cookie('font_weight', font_weight)
        return resp

    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_weight = request.cookies.get('font_weight')
    return render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, font_weight=font_weight)

@lab3.route('/lab3/clear_settings_cookies/', methods=['POST'])
def clear_settings_cookies():
    resp = make_response(redirect(url_for('lab3.settings')))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_weight')
    return resp

@lab3.route('/lab3/form_railway/')
def form_railway():
    return render_template('lab3/form_railway.html')

@lab3.route('/lab3/ticket/', methods=['POST'])
def ticket():
    fio = request.form['fio']
    berth = request.form['berth']
    linen = 'linen' in request.form
    baggage = 'baggage' in request.form
    age = int(request.form['age'])
    departure = request.form['departure']
    destination = request.form['destination']
    date = request.form['date']
    insurance = 'insurance' in request.form

    # Проверка возраста
    if age < 1 or age > 120:
        return "Возраст должен быть от 1 до 120 лет", 400

    # Расчет стоимости билета
    if age < 18:
        ticket_type = "Детский билет"
        price = 700
    else:
        ticket_type = "Взрослый билет"
        price = 1000

    if berth in ['нижняя', 'нижняя боковая']:
        price += 100

    if linen:
        price += 75

    if baggage:
        price += 250

    if insurance:
        price += 150

    return render_template('lab3/ticket.html', fio=fio, berth=berth, linen=linen, baggage=baggage, age=age,
                           departure=departure, destination=destination, date=date, insurance=insurance,
                           ticket_type=ticket_type, price=price)

products = [
    {"name": "iPhone 15", "price": 70000, "brand": "Apple", "color": "Черный"},
    {"name": "Samsung Galaxy S24", "price": 80000, "brand": "Samsung", "color": "Белый"},
    {"name": "Xiaomi Mi 11", "price": 60000, "brand": "Xiaomi", "color": "Синий"},
    {"name": "OnePlus 9", "price": 65000, "brand": "OnePlus", "color": "Красный"},
    {"name": "Google Pixel 5", "price": 75000, "brand": "Google", "color": "Зеленый"},
    {"name": "Huawei P40", "price": 70000, "brand": "Huawei", "color": "Желтый"},
    {"name": "Sony Xperia 1 II", "price": 90000, "brand": "Sony", "color": "Фиолетовый"},
    {"name": "Oppo Find X3", "price": 85000, "brand": "Oppo", "color": "Оранжевый"},
    {"name": "Vivo X60", "price": 55000, "brand": "Vivo", "color": "Серый"},
    {"name": "Realme GT", "price": 50000, "brand": "Realme", "color": "Коричневый"},
    {"name": "Nokia 8.3", "price": 45000, "brand": "Nokia", "color": "Золотой"},
    {"name": "Asus ROG Phone 5", "price": 95000, "brand": "Asus", "color": "Серебряный"},
    {"name": "Motorola Edge+", "price": 70000, "brand": "Motorola", "color": "Розовый"},
    {"name": "LG Velvet", "price": 60000, "brand": "LG", "color": "Бирюзовый"},
    {"name": "ZTE Axon 30", "price": 50000, "brand": "ZTE", "color": "Лаймовый"},
    {"name": "Lenovo Legion Phone Duel", "price": 80000, "brand": "Lenovo", "color": "Мятный"},
    {"name": "Meizu 18", "price": 55000, "brand": "Meizu", "color": "Бордовый"},
    {"name": "Honor 30 Pro+", "price": 65000, "brand": "Honor", "color": "Сливовый"},
    {"name": "Alcatel 3L", "price": 15000, "brand": "Alcatel", "color": "Шоколадный"},
    {"name": "BlackBerry Key2", "price": 40000, "brand": "BlackBerry", "color": "Кремовый"}
]

@lab3.route('/lab3/search_form/')
def form():
    return render_template('lab3/search_form.html')

@lab3.route('/lab3/products/', methods=['POST'])
def products_view():
    min_price = int(request.form['min_price'])
    max_price = int(request.form['max_price'])

    filtered_products = [product for product in products if min_price <= product['price'] <= max_price]

    return render_template('lab3/products.html', products=filtered_products)
