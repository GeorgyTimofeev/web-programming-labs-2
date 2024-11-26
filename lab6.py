from os import close
from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session, current_app
from flask.cli import main
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path
from lab5 import db_connect, db_close

lab6 = Blueprint('lab6',__name__)

@lab6.context_processor
def inject_current_lab():
    return {'current_lab': '/lab6/'}

def get_offices():
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT o.number, o.price, o.is_booked, u.login AS tenant FROM offices o LEFT JOIN users u ON o.tenant_id = u.id ORDER BY o.number")
    else:
        cur.execute("SELECT o.number, o.price, o.is_booked, u.login AS tenant FROM offices o LEFT JOIN users u ON o.tenant_id = u.id ORDER BY o.number")
    rows = cur.fetchall()
    db_close(conn, cur)

    # Преобразование объектов sqlite3.Row в словари
    offices = [dict(row) for row in rows]

    return offices

def update_office_booking(office_number, tenant_id, is_booked):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE offices SET tenant_id = %s, is_booked = %s WHERE number = %s", (tenant_id, is_booked, office_number))
    else:
        cur.execute("UPDATE offices SET tenant_id = ?, is_booked = ? WHERE number = ?", (tenant_id, is_booked, office_number))
    db_close(conn, cur)

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    if data['method'] == 'info':
        user_total_cost = 0
        login = session.get('login')
        offices = get_offices()
        if login:
            for office in offices:
                if office['tenant'] == login:
                    user_total_cost += office['price']
        return {
            'jsonrpc': '2.0',
            'result': {
                'offices': offices,
                'user_total_cost': user_total_cost
            },
            'id': id
        }
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    if data['method'] == 'booking':
        office_number = data['params']
        offices = get_offices()
        for office in offices:
            if office['number'] == office_number:
                if office['is_booked']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Office already booked'
                        },
                        'id': id
                    }
                user_id = get_user_id_by_login(login)
                update_office_booking(office_number, user_id, True)
                return {
                    'jsonrpc': '2.0',
                    'result': 'Success',
                    'id': id
                }

    if data['method'] == 'cancellation':
        office_number = data['params']
        offices = get_offices()
        for office in offices:
            if office['number'] == office_number:
                if not office['is_booked']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office not booked'
                        },
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Cannot cancel booking of another user'
                        },
                        'id': id
                    }
                update_office_booking(office_number, None, False)
                return {
                    'jsonrpc': '2.0',
                    'result': 'Success',
                    'id': id
                }
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }

def get_user_id_by_login(login):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?", (login,))
    user_id = cur.fetchone()['id']
    db_close(conn, cur)
    return user_id
