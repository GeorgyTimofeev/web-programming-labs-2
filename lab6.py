from os import close
from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session, current_app
from flask.cli import main
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

lab6 = Blueprint('lab6',__name__)

@lab6.context_processor
def inject_current_lab():
    return {'current_lab': '/lab6/'}

offices = []
for i in range (1, 11):
    offices.append({"number": i, "tenant": "", "price": 800+round((i**4)*3/2)})

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
        for office in offices:
            if office['number'] == office_number:
                if office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Office already booked'
                        },
                        'id': id
                    }

                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'Success',
                    'id': id
                }

    if data['method'] == 'cancellation':
        office_number = data['params']
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if not office['tenant']:
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
                office['tenant'] = ""
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
