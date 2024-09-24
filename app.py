from flask import Flask, url_for, redirect, abort
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(err):
    return '''Ошибка 400.
    Неверный запрос. Сервер не может или не будет обрабатывать запрос из-за чего-то,
    что воспринимается как ошибка клиента (например, неправильный синтаксис, формат
    или маршрутизация запроса).''', 400

@app.route('/lab1/trigger_400')
def trigger_400():
    abort(400)

@app.errorhandler(401)
def unauthorized(err):
    return '''Ошибка 401. Для доступа к ресурсу требуется аутентификация.
    Клиент должен передать заголовок Authorization в запросе.''', 401

@app.route('/lab1/trigger_401')
def trigger_401():
    abort(401)

class PaymentRequired(HTTPException):
    code = 402
    description = 'Payment Required'

@app.errorhandler(PaymentRequired)
def payment_required(err):
    return '''Ошибка 402. Зарезервировано для будущего использования.
    Используется для целей тестирования оплаты.''', 402

@app.route('/lab1/trigger_402')
def trigger_402():
    raise PaymentRequired()

@app.errorhandler(403)
def forbidden(err):
    return '''Ошибка 403. Клиент не имеет прав доступа к содержимому,
    поэтому сервер отказывает в выполнении запроса.''', 403

@app.route('/lab1/trigger_403')
def trigger_403():
    abort(403)

@app.errorhandler(404)
def not_found(err):
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
        <tytle>Ошибка 404</tytle>
    </head>
    <body>
        <h1>Упс… Кажется такой страницы не существует</h1>
        <p>Сервер не может найти запрошенный ресурс. В браузере это означает,
        что URL-адрес не распознан. В API это также может означать,
        что адрес правильный, но ресурс не существует.</p>

        <img src="''' + url_for('static', filename='Error_404_img.png') + '''" style="width: 300px;
        position: absolute; top: 60%; right: 50px; transform: translateY(-50%);"></br>

        <a href="/">Вернуться на главную</a>
    </body>
''', 404

@app.route('/lab1/trigger_404')
def trigger_404():
    abort(404)

@app.errorhandler(405)
def method_not_allowed(err):
    return '''Ошибка 405. Метод, указанный в запросе (например, POST, PUT, DELETE) не применим к ресурсу,
    и сервер не поддерживает его.''', 405

@app.route('/lab1/trigger_405')
def trigger_405():
    abort(405)

@app.errorhandler(418)
def i_am_a_teapot(err):
    return '''Ошибка 418. Я… я – чай? Определенный в RFC 2324. Этот код составляет часть
    апрельской шутки и не должен использоваться для серьезных целей.''', 418

@app.route('/lab1/trigger_418')
def trigger_418():
    abort(418)

@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
        <tytle>Ошибка 500</tytle>
    </head>
    <body>
        <h1>Внутренняя ошибка сервера</h1>
        <p>На сервере произошла ошибка, в результате которой он не может успешно обработать запрос.
        Пожалуйста, попробуйте позже.</p>

        <img src="''' + url_for('static', filename='Error_500_img.png') + '''" style="width: 300px;
        position: absolute; top: 50%; right: 100px; transform: translateY(-50%);"></br>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 500

@app.route('/lab1/trigger_500')
def trigger_500():
    abort(500)

@app.route('/lab1/an_error')
def make_an_error():
    return 1 / 0

@app.route('/')
@app.route('/index')
def index():
    return '''
<!doctype html>
<html>
    <head>
        <tytle>НГТУ, ФБ, Лабораторные работы</tytle>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</header>
        <ol>
            <li><a href="/lab1">Первая Лабораторная</a></li>
        </ol>
    </body>
    <footer>
        Тимофеев Георгий Алексеевич, ФБИ-22, 3 Курс, 2024 год.
    </footer>
</html>
'''

@app.route('/lab1')
def lab1():
    return'''
<!doctype html>
<html>
    <head>
        <tytle>Лабораторная 1</tytle>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
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

@app.route('/lab1/web')
def web():
    return '''<!doctype html>
        <html>
           <head>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
            </head>
           <body>
               <h1>web-сервер на flask</h1>
                <a href="/lab1/author">Автор</a>
           </body>
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route('/lab1/author')
def author():
    name = "Тимофеев Георгий Алексеевич"
    group = "ФБИ-22"
    faculty = "ФБ"

    return '''<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
            </head>
            <body>
                <p>Студент: ''' + name + '''</p>
                <p>Группа: ''' + group + '''</p>
                <p>Факультет: ''' + faculty + '''</p>
                <a href="/lab1/web">На страницу "web"</a>
            </body>
        </html>'''

@app.route('/lab1/oak')
def oak():
    path = url_for('static', filename='oak.jpg')
    style = url_for('static', filename='lab1.css')
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
@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>Счётчик</h1>
        <p>Сколько раз вы заходили на эту страницу: ''' + str(count) + '''</p>
        <a href="/lab1/counter_cleaner">Обнулить счётчик</a>
    </body>
</html>
'''

@app.route('/lab1/counter_cleaner')
def counter_cleaner():
    global count
    count = 0
    return redirect('/lab1/counter')

@app.route('/lab1/info')
def info():
    return redirect('/lab1/author')

tree_planted = False

# Обработчик для главной страницы /lab1/resource, которая показывает статус ресурса
@app.route('/lab1/resource')
def resource_status():
    global tree_planted
    if tree_planted:
        status_message = "Дерево посажено"
        status_image = url_for('static', filename='tree_after.jpg')
    else:
        status_message = "Дерево не посажено"
        status_image = url_for('static', filename='tree_before.jpg')

    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Состояние дерева</title>
            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='lab1.css')}">
        </head>
        <body>
            <h1>{status_message}</h1>
            <div class="text_container" style='width: 50%'>
                <ul>
                    <li><a href="{url_for('created')}">Посадить дерево</a></li>
                    <li><a href="{url_for('delete')}">Спилить дерево…</a></li>
                </ul>
                <a href="{url_for('lab1')}">Вернуться на страницу лабораторной</a>
            </div>
            <div class="image_container" style='position: absolute; right: 50px; top: 10%'>
                <img src="{status_image}">
            </div>
        </body>
    </html>
    '''

# Обработчик для создания ресурса /lab1/created
@app.route('/lab1/created')
def created():
    global tree_planted
    if tree_planted:
        return '''
        <!doctype html>
        <html>
            <head>
                <title>Отказано</title>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
            </head>
            <body style='background-image: url("''' + url_for('static', filename='big_tree.jpeg') +'''")'>
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
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
            </head>
            <body>
                <h1>Вы посадили дерево, Браво!</h1>
                <a href="/lab1/resource">Вернуться к состоянию дерева</a></br>
                <img src="''' + url_for('static', filename='tree_tumb_up.png') + '''" style='margin-top: 10px'>
            </body>
        </html>
        ''', 201


# Обработчик для удаления ресурса /lab1/delete
@app.route('/lab1/delete')
def delete():
    global tree_planted
    if tree_planted:
        tree_planted = False
        return '''
        <!doctype html>
        <html>
            <head>
                <title>Успешно</title>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
            </head>
            <body>
                <h1>Что вы наделали… Дерева больше нет…</h1>
                <a href="/lab1/resource">Вернуться к состоянию дерева</a></br>
                <img src="''' + url_for('static', filename='tree_tumb_down.png') + '''" style='margin-top: 10px'>
            </body>
        </html>
        ''', 200
    else:
        return '''
        <!doctype html>
        <html>
            <head>
                <title>Отказано</title>
                <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
            </head>
            <body style='background-image: url("''' + url_for('static', filename='no_trees_gleb.jpg') +'''"); background-size: cover; background-position: center; background-repeat: no-repeat; margin: 50px; padding: 0; height: 70vh;'>
                <h1>Тут больше нечего пилить</h1>
                <a href="/lab1/resource">Вернуться к состоянию дерева</a></br>
            </body>
        </html>
        ''', 400

@app.route('/lab1/new_route')
def new_route():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
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
            <img src="''' + url_for('static', filename='Sigmaringen_Castle.jpeg') + '''"></br>
            <img src="''' + url_for('static', filename='Sigmaringen_Castle_2.jpeg') + '''" style='margin-top: 10px'>
        </div>
    </body>
    <footer>Тимофеев Георгий Алексеевич, ФБИ-22, 3 Курс, 2024 год.</footer>
</html>
''', 200, {
    'Content-Language': 'en',
    'X-Nerd': '42',
    'X-Student': 'Timofeev Georgy'
}

@app.route('/lab2/a')
def a_no_slash():
    return 'без слеша'

@app.route('/lab2/a/')
def a_slash():
    return 'со слешем'

flower_list = ['Роза', 'Лилия', 'Тюльпан', 'Орхидея', 'Пион', 'Астра', 'Георгин', 'Хризантема', 'Гвоздика', 'Ирис']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return 'Цветок с таким id не найден', 404
    else:
        return "Цветок: " + flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Теперь в списке цветков есть: {name} </p>
        <p>Всего цветков: {len(flower_list)}</p>
        <p>Полный список цветков: {flower_list}</p>
    </body>
</html>
'''
