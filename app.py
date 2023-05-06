from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)

mail = ""
password = ""

@app.route('/')
def hello() -> str:
    return "WELCOME TO ROOMATE FINDER"

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit', methods = ['POST'])
def search():
    #do something
    db = sqlite3.connect('temp.db')
    mail = request.form['email']
    password = request.form['password']
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name=?", ('members',))
    result = cursor.fetchone()
    db.close()
    if(result is not None):
        db = sqlite3.connect('temp.db')
        cursor = db.cursor()
        cursor.execute('''SELECT password FROM members WHERE email =?''', (mail,))
        x = cursor.fetchall()
        if(len(x) != 0):
            if(x[0][0] == password):
                db.close()
                # redirect to search page
                return "Email exists"
            else:
                db.close()
                # put a message for wrong password
                return "Wrong Password"
        else:
            # put a message for Sign up 
            return "Email does not exist"
    else:
        db = sqlite3.connect('temp.db')
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE members(email varchar(100) PRIMARY KEY, password varchar(100))''')
        db.close()
        db = sqlite3.connect('temp.db')
        cursor = db.cursor()
        cursor.execute("INSERT into members(email, password) VALUES (?, ?)", (mail, password))
        db.commit()
        db.close()
        return "Email inserted"
    
if __name__ == "__main__":
    app.run(debug=True)