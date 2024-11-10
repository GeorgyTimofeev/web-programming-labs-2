from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session
lab5 = Blueprint('lab5',__name__)

@lab5.context_processor
def inject_current_lab():
    return {'current_lab': '/lab5/'}

@lab5.route('/lab5/')
def lab():
    name = session.get('name')
    login = session.get('login')
    return render_template('lab5/lab5.html', name=name, login=login)

@lab5.route('/lab5/login/', methods=['GET', 'POST'])
def login():
    return redirect(url_for('lab4.login'))

@lab5.route('/lab5/logout/', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect(url_for('lab4.login'))

@lab5.route('/lab5/register/',  methods=['GET', 'POST'])
def register():
    return redirect(url_for('lab4.register'))
