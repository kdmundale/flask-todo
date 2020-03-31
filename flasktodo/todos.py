import os
import psycopg2
import psycopg2.extras
from datetime import datetime

from flask import Blueprint, render_template, request, session, g, redirect, url_for

from . import db


bp = Blueprint("todos", __name__)

#Function for creating a new task in the DB
def create_new_task(cur):
    if request.method == 'POST':
        if 'action' in request.form:

            new_task = request.form['action']

            cur.execute('INSERT INTO todos (description, completed, created_at) VALUES (%s, %s, %s)',
            (new_task, False, datetime.now()))
            g.db.commit()


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
            create_new_task(cur)
            cur.execute('SELECT * FROM todos')
            todos = cur.fetchall()
            cur.close()

    return render_template("index.html", todos=todos)

@bp.route("/switch", methods=('GET', 'POST'))
def switch():
    """View for switching attribute completed to true for tasks."""

    if request.method == 'POST':
        id = request.args['id']

        cur = db.get_db().cursor()

        cur.execute(
         'UPDATE todos SET completed=(%s)'
         'WHERE id = (%s)',
         ('True', id));

        g.db.commit()

        cur.close()

    return redirect(url_for('todos.index'))

@bp.route("/delete", methods=('GET', 'POST'))
def delete():

    if request.method =='POST':
        id = request.args['id']

        cur = db.get_db().cursor()

        cur.execute(
         'DELETE FROM todos '
         'WHERE id = (%s)',
         (id,));

        g.db.commit()

        cur.close()

    return redirect(url_for('todos.index'))


@bp.route("/completed", methods=['GET', 'POST'])
def show_completed():
    """View for specific completed tasks."""

    cur = db.get_db().cursor()

    create_new_task(cur)

    cur.execute('SELECT * FROM todos WHERE completed = true')
    todos = cur.fetchall()
    cur.close()

    return render_template('index.html', todos=todos)


@bp.route("/unfinished", methods=['GET', 'POST'])
def show_unfinished():
    """View for specific unfinished tasks."""

    cur = db.get_db().cursor()

    create_new_task(cur)

    cur.execute('SELECT * FROM todos WHERE completed = false')
    todos = cur.fetchall()
    cur.close()

    return render_template('index.html', todos=todos)
