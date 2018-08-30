from flask import Flask, render_template, request, json
import sqlite3
app = Flask(__name__)

conn = sqlite3.connect('todolist.db')
print "Opened Database Successfully"

conn.close()

@app.route("/")

def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['GET', 'POST'])
def signUp() :
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']



if __name__ == "__main__":
    app.run()
