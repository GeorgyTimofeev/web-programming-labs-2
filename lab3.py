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
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')

    if request.args.get('clear'):
        resp = make_response(redirect(url_for('lab3.form1')))
        resp.set_cookie('user', '', expires=0)
        resp.set_cookie('age', '', expires=0)
        resp.set_cookie('sex', '', expires=0)
        return resp

    if user or age or sex:
        resp = make_response(render_template('lab3/form1.html', user=user, age=age, sex=sex))
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
    return render_template('lab3/form1.html', user=user, age=age, sex=sex)