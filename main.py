from flask import Flask, session, render_template, request, redirect, g, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route('/')
def index():
    # if request.method == 'POST':
    #     session.pop('user', None)
    #
    #     if request.form['password'] == 'password':
    #         session['user'] = request.form['username']
    #         return redirect(url_for('protected'))
    #
    # return render_template('index.html')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        try:
            username = request.form['username']
            password = request.form['password']

            with sql.connect("users") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user (username, password) VALUES (?,?)",(username,password))

                con.commit()
        except:
            con.rollback()

        finally:
            return redirect(url_for("login"))
            con.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username,password)
        if completion == False:
            error = 'Invalid Credentials'
        else:
            return redirect(url_for('protected'))
    return render_template('login.html', error=error)

def validate(username, password):
    completion = False
    with sql.connect("users") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM user")
        rows = cur.fetchall()
        for row in rows:
            dbUser = row[0]
            dbPass = row[1]
            if dbUser == username:
                completion=True
    return completion



@app.route('/protected')
def protected():
    return redirect(url_for('tasks_list'))



@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'Not logged in!'

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return 'Dropped!'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False

    def __repr__(self):
        return '<Content %s>' % self.content


db.create_all()


@app.route('/taskall')
def tasks_list():
    tasks = Task.query.all()
    return render_template('list.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/taskall')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/taskall')

    db.session.delete(task)
    db.session.commit()
    return redirect('/taskall')


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/taskall')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/taskall')

if __name__ == '__main__':
    app.run(debug=True)
