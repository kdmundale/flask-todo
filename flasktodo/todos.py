import os
import psycopg2
import psycopg2.extras
from datetime import datetime
from flask import Blueprint, render_template, request, session, g, redirect, url_for 

from . import db


bp = Blueprint("todos", __name__)


@bp.route("/", methods=['GET', 'POST'])
def index():
    """View for home page which shows list of to-do items."""

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()

    if request.method == 'POST':
        new_task = request.form['action']
        if new_task =='':
            pass
        else:
            cur.execute('INSERT INTO todos (description, completed, created_at) VALUES (%s, %s, %s)',
                    (new_task, False, datetime.now()))
            g.db.commit()
            cur.execute('SELECT * FROM todos')
            todos = cur.fetchall()
            cur.close()

    return render_template("index.html", todos=todos)

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

@bp.route("/edit", methods=['GET', 'POST'])
def update():
    id = request.args['id']
    cur = db.get_db().cursor()
    cur.execute('SELECT description FROM todos WHERE id = (%s)',
            (id,))
    description = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        new_description = request.form['description']
        cur = db.get_db().cursor()
        cur.execute(
            "UPDATE todos SET description=(%s)"
            " WHERE id=(%s)",
            (new_description, id,));
        g.db.commit()
        return redirect(url_for('todos.index'))

    return render_template("edit.html", description=description)
