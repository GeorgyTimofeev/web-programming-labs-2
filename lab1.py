from flask import Blueprint, url_for, redirect, abort, render_template, request
from werkzeug.exceptions import HTTPException
lab1 = Blueprint('lab1',__name__)

@lab1.context_processor
def inject_current_lab():
    return {'current_lab': '/lab1/'}

@lab1.route('/lab1/trigger_400')
def trigger_400():
    abort(400)


@lab1.route('/lab1/trigger_401')
def trigger_401():
    abort(401)


class PaymentRequired(HTTPException):
    code = 402
    description = 'Payment Required'


@lab1.route('/lab1/trigger_402')
def trigger_402():
    raise PaymentRequired()


@lab1.route('/lab1/trigger_403')
def trigger_403():
    abort(403)


@lab1.route('/lab1/trigger_404')
def trigger_404():
    abort(404)


@lab1.route('/lab1/trigger_405')
def trigger_405():
    abort(405)


@lab1.route('/lab1/trigger_418')
def trigger_418():
    abort(418)


@lab1.route('/lab1/trigger_500')
def trigger_500():
    abort(500)


@lab1.route('/lab1/an_error')
def make_an_error():
    try:
        result = 1 / 0
    except ZeroDivisionError:
        abort(500)
    return str(result)


@lab1.route('/lab1')
def lab():
    return'''
<!doctype html>
<html>
    <head>
        <tytle>Лабораторная 1</tytle>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
    </head>
    <body>
        <h1>Flask</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python,
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится
        к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений,
        сознательно предоставляющих лишь самые базовые возможности.</p>

        <a href="/">Назад на главную</a></li>

        <div class="container" style='display: flex; justify-content: space-between;'>
            <div class="rout_list" style='width: 30%; margin-left: 5px'>
                <h2>Список rout'ов:</h2>
                <ol>
                    <li><a href="/index">/index</a></li>
                    <li><a href="/lab1/web">/lab1/web</a></li>
                    <li><a href="/lab1/info">/lab1/info</a></li>
                    <li><a href="/lab1/oak">/lab1/oak</a></li>
                    <li><a href="/lab1/counter">/lab1/counter</a></li>
                    <li><a href="/lab1/new_route">/lab1/new_route</a></li>
                    <li><a href="/lab1/resource">/lab1/resource (дополнительное задание)</a></li>
                </ol>
            </div>

            <div class="error_list" style='width: 68%;'>
                <h2>Список ошибок:</h2>
                <ol>
                    <li><a href="/lab1/trigger_400">400</a></li>
                    <li><a href="/lab1/trigger_401">401</a></li>
                    <li><a href="/lab1/trigger_402">402</a></li>
                    <li><a href="/lab1/trigger_403">403</a></li>
                    <li><a href="/lab1/trigger_404">404</a></li>
                    <li><a href="/lab1/trigger_405">405</a></li>
                    <li><a href="/lab1/trigger_418">418</a></li>
                    <li><a href="/lab1/trigger_500">500</a></li>
                </ol>
            </div>
        </div>
    </body>
    <footer>
        Тимофеев Георгий Алексеевич, ФБИ-22, 3 Курс, 2024 год.
    </footer>
</html>
'''


@lab1.route('/lab1/web')
def web():
    return '''<!doctype html>
        <html>
           <head>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
            </head>
           <body>
               <h1>web-сервер на flask</h1>
                <a href="/lab1/author">Автор</a>
           </body>
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route('/lab1/author')
def author():
    name = "Тимофеев Георгий Алексеевич"
    group = "ФБИ-22"
    faculty = "ФБ"

    return '''<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
            </head>
            <body>
                <p>Студент: ''' + name + '''</p>
                <p>Группа: ''' + group + '''</p>
                <p>Факультет: ''' + faculty + '''</p>
                <a href="/lab1/web">На страницу "web"</a>
            </body>
        </html>'''


@lab1.route('/lab1/oak')
def oak():
    path = url_for('static', filename='lab1/oak.jpg')
    style = url_for('static', filename='lab1/lab1.css')
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''


count = 0
@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
    </head>
    <body>
        <h1>Счётчик</h1>
        <p>Сколько раз вы заходили на эту страницу: ''' + str(count) + '''</p>
        <a href="/lab1/counter_cleaner">Обнулить счётчик</a>
    </body>
</html>
'''


@lab1.route('/lab1/counter_cleaner')
def counter_cleaner():
    global count
    count = 0
    return redirect('/lab1/counter')


@lab1.route('/lab1/info')
def info():
    return redirect('/lab1/author')


tree_planted = False

# Обработчик для главной страницы /lab1/resource, которая показывает статус ресурса
@lab1.route('/lab1/resource')
def resource_status():
    global tree_planted
    if tree_planted:
        status_message = "Дерево посажено"
        status_image = url_for('static', filename='lab1/tree_after.jpg')
    else:
        status_message = "Дерево не посажено"
        status_image = url_for('static', filename='lab1/tree_before.jpg')

    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Состояние дерева</title>
            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='lab1/lab1.css')}">
        </head>
        <body>
            <h1>{status_message}</h1>
            <div class="text_container" style='width: 50%'>
                <ul>
                    <li><a href="{url_for('lab1.created')}">Посадить дерево</a></li>
                    <li><a href="{url_for('lab1.delete')}">Спилить дерево…</a></li>
                </ul>
                <a href="{url_for('lab1.lab')}">Вернуться на страницу лабораторной</a>
            </div>
            <div class="image_container" style='position: absolute; right: 50px; top: 10%'>
                <img src="{status_image}">
            </div>
        </body>
    </html>
    '''


# Обработчик для создания ресурса /lab1/created
@lab1.route('/lab1/created')
def created():
    global tree_planted
    if tree_planted:
        return '''
        <!doctype html>
        <html>
            <head>
                <title>Отказано</title>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
            </head>
            <body style='background-image: url("''' + url_for('static', filename='lab1/big_tree.jpeg') +'''")'>
                <h1 style='color: white; width: 50%'>Дерево уже посажено и прекрасно себя чувствует</h1>
                <a href="/lab1/resource" style='color: white'>Вернуться к состоянию дерева</a></br>
            </body>
        </html>
        ''', 400
    else:
        tree_planted = True
        return '''
        <!doctype html>
        <html>
            <head>
                <title>Успешно</title>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
            </head>
            <body>
                <h1>Вы посадили дерево, Браво!</h1>
                <a href="/lab1/resource">Вернуться к состоянию дерева</a></br>
                <img src="''' + url_for('static', filename='lab1/tree_tumb_up.png') + '''" style='margin-top: 10px'>
            </body>
        </html>
        ''', 201


# Обработчик для удаления ресурса /lab1/delete
@lab1.route('/lab1/delete')
def delete():
    global tree_planted
    if tree_planted:
        tree_planted = False
        return '''
        <!doctype html>
        <html>
            <head>
                <title>Успешно</title>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
            </head>
            <body>
                <h1>Что вы наделали… Дерева больше нет…</h1>
                <a href="/lab1/resource">Вернуться к состоянию дерева</a></br>
                <img src="''' + url_for('static', filename='lab1/tree_tumb_down.png') + '''" style='margin-top: 10px'>
            </body>
        </html>
        ''', 200
    else:
        return '''
        <!doctype html>
        <html>
            <head>
                <title>Отказано</title>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
            </head>
            <body style='background-image: url("''' + url_for('static', filename='lab1/no_trees_gleb.jpg') +'''"); background-size: cover; background-position: center; background-repeat: no-repeat; margin: 50px; padding: 0; height: 70vh;'>
                <h1>Тут больше нечего пилить</h1>
                <a href="/lab1/resource">Вернуться к состоянию дерева</a></br>
            </body>
        </html>
        ''', 400


@lab1.route('/lab1/new_route')
def new_route():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1/lab1.css') + '''">
        <tytle>Sigmaringen Castle</tytle>
    </head>
    <body>
        <p>From Wikipedia, the free encyclopedia</p>
        <div class="text_container" style='width: 50%'>
            <p style='margin-top: 10px'><b>Sigmaringen Castle</b> (German: Schloss Sigmaringen) was the princely castle and seat
            of government for the Princes of Hohenzollern-Sigmaringen. Situated in the Swabian Alb region
            of Baden-Württemberg, Germany, this castle dominates the skyline of the town of Sigmaringen.
            The castle was rebuilt following a fire in 1893, and only the towers of the earlier medieval
            fortress remain. Schloss Sigmaringen was a family estate of the Swabian Hohenzollern family,
            a cadet branch of the Hohenzollern family, from which the German Emperors and kings of
            Prussia came. During the closing months of World War II, Schloss Sigmaringen was briefly
            the seat of the Vichy French Government after France was liberated by the Allies.
            The castle and museums may be visited throughout the year, but only on guided tours.
            It is still owned by the Hohenzollern-Sigmaringen family, although they
            no longer reside there.</p>

            <h1>Location</h1>
            <p>Sigmaringen is located on the southern edge of the Swabian Jura,
            a plateau region in southern Baden-Württemberg. The Hohenzollern
            castle was built below the narrow Danube river valley in the modern
            Upper Danube Nature Park (German: Naturpark Obere Donau). The castle
            rises above the Danube on a towering chalk projection that is a spur of
            the white Jura Mountains formation. The hill is known simply as the
            Schlossberg or Castle Rock. The Schlossberg is about 200 meters (660 ft)
            long and up to 35 meters (115 ft) above the river. On this free-standing
            towering rock, the princely Hohenzollern castle is the largest of the Danube
            valley castles. The sheer cliffs and steep sides of the tower made it a
            natural site for a well-protected medieval castle.</p>

            <a href="/lab1">Назад на страницу лабораторной</a>
        </div>

        <div class="image_container" style='position: absolute; right: 50px; top: 10%'>
            <img src="''' + url_for('static', filename='lab1/Sigmaringen_Castle.jpeg') + '''"></br>
            <img src="''' + url_for('static', filename='lab1/Sigmaringen_Castle_2.jpeg') + '''" style='margin-top: 10px'>
        </div>
    </body>
    <footer>Тимофеев Георгий Алексеевич, ФБИ-22, 3 Курс, 2024 год.</footer>
</html>
''', 200, {
    'Content-Language': 'en',
    'X-Nerd': '42',
    'X-Student': 'Timofeev Georgy'
}
