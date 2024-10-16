from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response
lab3 = Blueprint('lab3',__name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    user = request.args.get('user')
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
