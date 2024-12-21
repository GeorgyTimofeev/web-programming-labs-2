from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session, current_app, flash, jsonify
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

from werkzeug.security import check_password_hash, generate_password_hash
from lab5 import db_connect, db_close
from db import db
from db.models import users, articles, favorites, offices

from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)

@lab8.context_processor
def inject_current_lab():
    return {'current_lab': '/lab8/'}

@lab8.route('/lab8/')
def lab():
    login = session.get('login')
    return render_template('lab8/lab8.html', login=login)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=False)

    session['login'] = login_form

    return redirect('/lab8/')

@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember_me') == 'on'

    user = users.query.filter_by(login=login_form).first()

    if user:
        if password_form and check_password_hash(user.password, password_form):
            login_user(user, remember=remember_me)
            session['login'] = login_form
            return redirect('/lab8/')

    return render_template('lab8/login.html', error="Ошибка входа: логин и/или пароль неверны")

@lab8.route('/lab8/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.pop('login', None)
    return redirect('/lab8/')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(user_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'

    if not (title and article_text):
        return render_template('lab8/create_article.html', error='Заполните все поля')

    new_article = articles(user_id=current_user.id, title=title, article_text=article_text, is_public=is_public, is_favorite=False, likes=0)
    db.session.add(new_article)
    db.session.commit()

    return redirect(url_for('lab8.article_list'))

@lab8.route('/lab8/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id, user_id=current_user.id).first()
    if not article:
        return render_template('lab8/create_article.html', error='Статья не найдена')

    if request.method == 'GET':
        return render_template('lab8/create_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'

    if not (title and article_text):
        return render_template('lab8/create_article.html', error='Заполните все поля', article=article)

    article.title = title
    article.article_text = article_text
    article.is_public = is_public
    db.session.commit()

    return redirect(url_for('lab8.article_list'))

@lab8.route('/lab8/delete/<int:article_id>/', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.filter_by(id=article_id, user_id=current_user.id).first()
    if not article:
        return redirect(url_for('lab8.article_list'))

    db.session.delete(article)
    db.session.commit()

    return redirect(url_for('lab8.article_list'))

@lab8.route('/lab8/public_articles/')
def public_articles():
    public_articles = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/public_articles.html', articles=public_articles)

@lab8.route('/lab8/search/', methods=['GET', 'POST'])
def search_articles():
    query = request.form.get('query')
    if query:
        if current_user.is_authenticated:
            search_results = articles.query.filter(
                (articles.title.ilike(f'%{query}%')) |
                (articles.article_text.ilike(f'%{query}%')),
                (articles.is_public == True) |
                (articles.user_id == current_user.id)
            ).all()
        else:
            search_results = articles.query.filter(
                (articles.title.ilike(f'%{query}%')) |
                (articles.article_text.ilike(f'%{query}%')),
                articles.is_public == True
            ).all()
    else:
        search_results = []

    return render_template('lab8/search.html', articles=search_results, query=query)
