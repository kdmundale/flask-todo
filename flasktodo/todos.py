from flask import Blueprint, render_template

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

    # if method=='POST':
    # def new_todo():
    #"""adds a new item to the todo list"""
    # Take the input from the form
    #new_item = request.form['action']
    # Insert new description into the table as a new row
    #cur = db.get_db().cursor()
    # cur.execute("INSERT INTO todos (description) VALUE (%)",
    # (new_item))

    # return updated table with submit button
