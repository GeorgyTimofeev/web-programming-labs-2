from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session
lab4 = Blueprint('lab4',__name__)

@lab4.context_processor
def inject_current_lab():
    return {'current_lab': '/lab4/'}

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html', current_lab='/lab4/')


@lab4.route('/lab4/div-form/')
def div_form():
    return render_template("lab4/div-form.html", type='Деление', type_symbol='/')

@lab4.route('/lab4/div/', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Введите оба числа')

    if x2 == '0':
        return render_template('lab4/div.html', error='На ноль делить нельзя!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result, type='Деление', type_symbol='/')

@lab4.route('/lab4/add-form/')
def add_form():
    return render_template("lab4/add-form.html", type='Сложение', type_symbol='+')

@lab4.route('/lab4/add/', methods = ['POST'])
def add():
    x1 = request.form.get('x1') or '0'
    x2 = request.form.get('x2') or '0'

    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/add.html', x1=x1, x2=x2, result=result, type='Сложение', type_symbol='+')

@lab4.route('/lab4/mul-form/')
def mul_form():
    return render_template("lab4/mul-form.html", type='Умножение', type_symbol='*')

@lab4.route('/lab4/mul/', methods = ['POST'])
def mul():
    x1 = request.form.get('x1') or '1'
    x2 = request.form.get('x2') or '1'

    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result, type='Умножение', type_symbol='*')

@lab4.route('/lab4/sub-form/')
def sub_form():
    return render_template("lab4/sub-form.html", type='Вычитание', type_symbol='-')

@lab4.route('/lab4/sub/', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Введите оба числа')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result, type='Вычитание', type_symbol='-')

@lab4.route('/lab4/pow-form/')
def pow_form():
    return render_template("lab4/pow-form.html", type='Возведение в степень', type_symbol='**')

@lab4.route('/lab4/pow/', methods = ['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Введите оба числа')

    if x1 == '0' and x2 == '0':
        return render_template('lab4/pow.html', error='0 в степени 0 не определено!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result, type='Возведение в степень', type_symbol='**')

tree_count = 0

@lab4.route('/lab4/tree/', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'plant':
        tree_count += 1
    elif operation == 'cut' and tree_count > 0:
        tree_count -= 1

    return redirect(url_for('lab4.tree'))

users = [
    {'login': 'georgy1337', 'password': '2209', 'name': 'Георгий Тимофеев', 'gender': 'male'},
    {'login': 'witch', 'password': '0209', 'name': 'Кристина Толкачева', 'gender': 'female'},
    {'login': 'predator2003', 'password': '2309', 'name': 'Иван Осягин', 'gender': 'male'},
    {'login': 'anya', 'password': '123', 'name': 'Анна', 'gender': 'female'},
    {'login': 'egg15', 'password': '0411', 'name': 'Егор Иванов', 'gender': 'male'},
    {'login': 'sonya_money_way', 'password': '2407', 'name': 'Соня', 'gender': 'female'}
]

@lab4.route('/lab4/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            name = session['name']
        else:
            authorized = False
            login = ''
            name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name)

    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect(url_for('lab4.login'))

    error = 'Неверный логин или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout/', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect(url_for('lab4.login'))

@lab4.route('/lab4/fridge/', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        if 'temperature' in session:
            temperature = session['temperature']
            if -12 <= temperature <= -9:
                message = f'Установлена температура: {temperature}°С'
                snowflakes = '❄️❄️❄️'
            elif -8 <= temperature <= -5:
                message = f'Установлена температура: {temperature}°С'
                snowflakes = '❄️❄️'
            elif -4 <= temperature <= -1:
                message = f'Установлена температура: {temperature}°С'
                snowflakes = '❄️'
            return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)
        return render_template('lab4/fridge.html')

    temperature = request.form.get('temperature')

    if not temperature:
        error = 'ошибка: не задана температура'
        return render_template('lab4/fridge.html', error=error)

    try:
        temperature = int(temperature)
    except ValueError:
        error = 'ошибка: некорректное значение температуры'
        return render_template('lab4/fridge.html', error=error)

    if temperature < -12:
        error = 'не удалось установить температуру — слишком низкое значение'
        return render_template('lab4/fridge.html', error=error)
    elif temperature > -1:
        error = 'не удалось установить температуру — слишком высокое значение'
        return render_template('lab4/fridge.html', error=error)
    elif -12 <= temperature <= -9:
        message = f'Установлена температура: {temperature}°С'
        snowflakes = '❄️❄️❄️'
    elif -8 <= temperature <= -5:
        message = f'Установлена температура: {temperature}°С'
        snowflakes = '❄️❄️'
    elif -4 <= temperature <= -1:
        message = f'Установлена температура: {temperature}°С'
        snowflakes = '❄️'

    session['temperature'] = temperature
    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)

@lab4.route('/lab4/grain-order/', methods=['GET', 'POST'])
def grain_order():
    grain_prices = {
        'Ячмень': 12345,
        'Овёс': 8522,
        'Пшеница': 8722,
        'Рожь': 14111
    }

    if request.method == 'GET':
        if 'grain_order' in session:
            order = session['grain_order']
            message = f'<b>Заказ успешно сформирован.</b><br>Вы заказали <u>{order["grain_type"]}.</u><br>Вес: {order["weight"]} т.<br>Сумма к оплате: <i>{order["total_price"]:.2f} руб</i>.'
            if order['discount'] > 0:
                message += f'<br>(применена скидка за большой объём: {order["discount"]:.2f} руб)'
            return render_template('lab4/grain-order.html', message=message, grain_prices=grain_prices)
        return render_template('lab4/grain-order.html', grain_prices=grain_prices)

    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')

    if not weight:
        error = 'Ошибка: вес не указан'
        return render_template('lab4/grain-order.html', error=error, grain_prices=grain_prices)

    try:
        weight = float(weight)
    except ValueError:
        error = 'Ошибка: некорректное значение веса'
        return render_template('lab4/grain-order.html', error=error, grain_prices=grain_prices)

    if weight <= 0:
        error = 'Ошибка: вес должен быть больше 0'
        return render_template('lab4/grain-order.html', error=error, grain_prices=grain_prices)

    if weight > 500:
        error = 'Ошибка: такого объёма сейчас нет в наличии'
        return render_template('lab4/grain-order.html', error=error, grain_prices=grain_prices)

    price_per_ton = grain_prices.get(grain_type)
    if not price_per_ton:
        error = 'Ошибка: некорректный тип зерна'
        return render_template('lab4/grain-order.html', error=error, grain_prices=grain_prices)

    total_price = weight * price_per_ton
    discount = 0

    if weight > 50:
        discount = total_price * 0.10
        total_price -= discount

    message = f'<b>Заказ успешно сформирован.</b><br>Вы заказали <u>{grain_type}.</u><br>Вес: {weight} т.<br>Сумма к оплате: <i>{total_price:.2f} руб</i>.'
    if discount > 0:
        message += f'<br>(применена скидка за большой объём: {discount:.2f} руб)'

    session['grain_order'] = {
        'grain_type': grain_type,
        'weight': weight,
        'total_price': total_price,
        'discount': discount
    }

    return render_template('lab4/grain-order.html', message=message, grain_prices=grain_prices)

@lab4.route('/lab4/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')
    gender = request.form.get('gender')

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/register.html', error=error)
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/register.html', error=error)
    if not name:
        error = 'Не введено имя'
        return render_template('lab4/register.html', error=error)
    if not gender:
        error = 'Не указан пол'
        return render_template('lab4/register.html', error=error)

    for user in users:
        if login == user['login']:
            error = 'Пользователь с таким логином уже существует'
            return render_template('lab4/register.html', error=error)

    new_user = {
        'login': login,
        'password': password,
        'name': name,
        'gender': gender
    }
    users.append(new_user)

    return redirect(url_for('lab4.login'))

@lab4.route('/lab4/users/', methods=['GET', 'POST'])
def users_list():
    if 'login' not in session:
        return redirect(url_for('lab4.login'))

    if request.method == 'POST':
        action = request.form.get('action')
        login = session['login']

        if action == 'delete':
            global users
            users = [user for user in users if user['login'] != login]
            session.pop('login', None)
            return redirect(url_for('lab4.login'))

        if action == 'edit':
            new_name = request.form.get('name')
            new_password = request.form.get('password')
            for user in users:
                if user['login'] == login:
                    if new_name:
                        user['name'] = new_name
                    if new_password:
                        user['password'] = new_password
                    session['name'] = user['name']
                    break

    return render_template('lab4/users.html', users=users)
