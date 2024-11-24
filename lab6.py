from os import close
from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session, current_app
from flask.cli import main
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

lab6 = Blueprint('lab6',__name__)

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')
