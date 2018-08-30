from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)





@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        try:
            _name = request.form['name']
            _email = request.form['email']
            _password = request.form['password']

            with sql.connect('users1') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO user(name, email, password) VALUES (?,?,?)", (_name, _email, _password))
                conn.commit()
                msg = "Successfully registered"
        except:
             conn.rollback()
             msg = "error in insert operation"

        finally:

            return render_template("test.html", msg = msg )
            conn.close()





if __name__ == "__main__":
    app.run(debug = True)
