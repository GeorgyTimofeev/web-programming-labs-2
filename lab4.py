from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response
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
