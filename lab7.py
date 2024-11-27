from os import close
from flask import Blueprint, url_for, redirect, abort, render_template, request, make_response, session, current_app
from flask.cli import main
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
