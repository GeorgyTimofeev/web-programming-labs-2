from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response
lab3 = Blueprint('lab3',__name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color)

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
