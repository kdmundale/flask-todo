from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flasktodo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = get_db().cursor()
        error = None

        if not email:
            error = 'email is required'
        elif not password:
            error = 'password is required'
        else:
            cur.execute(
                'SELECT id FROM users WHERE email = %s', (email,)
            )
            result = cur.fetchone()

            if result is not None:
                error = 'email not valid'

        if error is None:
            cur.execute(
                'INSERT INTO users (email, password) VALUES (%s, %s)',
                (email, generate_password_hash(password))
            )
            g.db.commit()
            cur.close()
            return redirect(url_for('auth.login'))

        cur.close()
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = get_db().cursor()
        error = None
        cur.execute(
            'SELECT * FROM users WHERE email = %s', (email,)
        )

        user = cur.fetchone()
        if user is None:
            error = ' incorrect login credentials '
        elif not check_password_hash(user['password'], password):
            error = ' incorrect login credentials '

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todos.index'))

        flash(error)

    return render_template('auth/login.html', message=error)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cur = get_db().cursor()
        cur.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user = cur.fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('todos.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
