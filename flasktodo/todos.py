from datetime import datetime

from flask import Blueprint, render_template, request, session

from . import db


bp = Blueprint("todos", __name__)


@bp.route("/", methods=['GET', 'POST'])
def index():
    """View for home page which shows list of to-do items."""

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)


@bp.route("/new", methods=['GET', 'POST'])
def new_todo():
    if request.method == 'POST':
        now = datetime.timetz()
        # """adds a new item to the todo list"""
        # Take the input from the form
        new_item = request.form['action']
    # Insert new description into the table as a new row
        cur = db.get_db().cursor()
        cur.execute("INSERT INTO todos (description, completed, created_at) VALUE (%,%,%)",
                    (new_item, False, now))
        cur.execute('SELECT * FROM todos')
        todos = cur.fetchall()
        cur.close()

    # return updated table with submit button
    return render_template("index.html")


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
