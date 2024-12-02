from os import close
from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session, current_app
from flask.cli import main
from datetime import datetime
from flask.templating import render_template_string
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path
from lab5 import db_connect, db_close

lab7 = Blueprint('lab7',__name__)

@lab7.context_processor
def inject_current_lab():
    return {'current_lab': '/lab7/'}

@lab7.route('/lab7/')
def main():
    return render_template("lab7/lab7.html")

films = [
    {
        "title": "mother!",
        "title_ru": "мама!",
        "year": 2017,
        "description": "Отношения молодой пары оказываются под угрозой, когда, нарушая безмятежное существование супругов, в их дом заявляются незваные гости.",
        "IMDB": 6.60

    },
    {
        "title": "Antichrist",
        "title_ru": "Антихрист",
        "year": 2009,
        "description": "Немолодая пара теряет сына - двухлетний мальчик падает из окна, когда родители занимаются любовью. Чувство вины буквально сводит с ума мать ребенка, его отец-психотерапевт пытается помочь жене и увозит её в старый дом в лесной чаще. Там супруги погружаются в мир странных символов, в их жизнь проникает безумие и насилие.",
        "IMDB": 6.50
    },

    {
        "title": "The Big Short",
        "title_ru": "Игра на понижение",
        "year": 2015,
        "description": "2005 год. Изучая данные ипотек по стране, чудаковатый финансовый гений и управляющий хедж-фонда Scion Capital Майкл Бьюрри обращает внимание на одну деталь и приходит к выводу, что американский рынок ипотечных кредитов может скоро лопнуть. В связи с этим он страхует около миллиарда долларов своих клиентов через кредитный дефолтный своп. Клиенты фонда Бьюрри волнуются из-за возможных потерь, ведь рынок ипотечных кредитов представляется весьма стабильным, но Майкл твёрдо стоит на своём. Вскоре эту странную активность замечают несколько финансистов на Уолл-стрит. Изучив данные, они осознают, что опасения Бьюрри имеют под собой веские основания. Более того, сыграв на понижение, можно заработать миллионы.",
        "IMDB": 7.80
    },
    {
        "title": "Drugstore Cowboy",
        "title_ru": "Аптечный ковбой",
        "year": 1989,
        "description": "В поисках наркотиков они грабят аптеки, убегают от полиции, и это похоже на игру - полицейские и воры. Главное - следить за приметами: ни в коем случае не говорить о собаках, не смотреться в зеркало с обратной стороны, и самое главное - никогда не класть шляпу на кровать. Для Боба наркотики - не просто способ получения удовольствия, скорее возможность убежать от невыносимой реальности жизни. Создать свой мир, где нет нудных обязанностей и глупых обывателей и где ты полновластный хозяин. В отличие от своих друзей, Боб знает, какую цену придется платить за это бегство, отсюда и вера в приметы. Но когда-нибудь игра закончится...",
        "IMDB": 7.20
    },

    {
        "title": "Le cercle rouge",
        "title_ru": "Красный круг",
        "year": 1970,
        "description": "Перед выходом на свободу известный преступник Коре получает от охранника наводку на модный ювелирный магазин. Освободившись, он наносит ночной визит бывшему партнёру Рико, из-за которого оказался в тюрьме, и грабит его. Преследуемый подручными Рико, Коре отправляется из Марселя в Париж и в пути спасает недавно сбежавшего бандита Вожеля, которого сопровождал к месту заключения комиссар Маттей. Два преступника становятся преданными друзьями и решают осуществить ограбление по наводке Коре, но матёрый и хитрый комиссар Маттей не дремлет.",
        "IMDB": 7.90
    },
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id > (len(films)-1) or id < 0:
        return abort(404)

    else:
        return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id > (len(films)-1) or id < 0:
        return abort(404)

    else:
        del films[id]
        return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    try:
        film = request.get_json()
        current_year = datetime.now().year
        if id > (len(films)-1) or id < 0:
            return {"error": "Фильм не найден"}, 404
        else:
            if "title" not in film and "title_ru" not in film:
                return {"title": "Заполните название или русское название"}, 400
            if "title_ru" not in film or film["title_ru"] == '':
                return {"title_ru": "Заполните русское название"}, 400
            if "title" not in film or film["title"] == '':
                film["title"] = film["title_ru"]
            if "year" not in film:
                return {"year": "Заполните год выпуска"}, 400
            try:
                year = int(film["year"])
            except ValueError:
                return {"year": "Год должен быть числом"}, 400
            if not (1895 <= year <= current_year):
                return {"year": "Год должен быть от 1895 до текущего года"}, 400
            if "description" not in film or film["description"] == '' or len(film["description"]) > 2000:
                return {"description": "Заполните описание (не более 2000 символов)"}, 400
            films[id] = film
            return film
    except Exception as e:
        return {"error": str(e)}, 500

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    try:
        new_film = request.get_json()
        current_year = datetime.now().year
        if "title" not in new_film and "title_ru" not in new_film:
            return {"title": "Заполните название или русское название"}, 400
        if "title_ru" not in new_film or new_film["title_ru"] == '':
            return {"title_ru": "Заполните русское название"}, 400
        if "title" not in new_film or new_film["title"] == '':
            new_film["title"] = new_film["title_ru"]
        if "year" not in new_film:
            return {"year": "Заполните год выпуска"}, 400
        try:
            year = int(new_film["year"])
        except ValueError:
            return {"year": "Год должен быть числом"}, 400
        if not (1895 <= year <= current_year):
            return {"year": "Год должен быть от 1895 до текущего года"}, 400
        if "description" not in new_film or new_film["description"] == '' or len(new_film["description"]) > 2000:
            return {"description": "Заполните описание (не более 2000 символов)"}, 400
        films.append(new_film)
        return {'id': len(films) - 1}, 201
    except Exception as e:
        return {"error": str(e)}, 500
