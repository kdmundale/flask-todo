import os
import psycopg2
import psycopg2.extras
from datetime import datetime

from flask import Blueprint, render_template, request, session, g

from . import db


bp = Blueprint("todos", __name__)


@bp.route("/", methods=['GET', 'POST'])
def index():
    """View for home page which shows list of to-do items."""
    cur = db.get_db().cursor()

    if request.method == 'POST':
        new_task = request.form['action']

        cur.execute('INSERT INTO todos (description, completed, created_at) VALUES (%s, %s, %s)',
                    (new_task, False, datetime.now()))
        g.db.commit()

    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()

    cur.close()

    return render_template("index.html", todos=todos)


@bp.route("/new", methods=['GET', 'POST'])
@bp.route("/completed", methods=['GET', 'POST'])
def show_completed():
    """View for specific completed tasks."""

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM todos WHERE completed = true')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)


@bp.route("/unfinished", methods=['GET', 'POST'])
def show_unfinished():
    """View for specific unfinished tasks."""

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM todos WHERE completed = false')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)
