from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello() -> str:
    return "WELCOME TO ROOMATE FINDER"

mail=""

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginn', methods = ['POST'])
def loginn():
    global mail
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
                return redirect(url_for('results'))
            else:
                db.close()
                error = True
                error_msg = 'Invalid password'
                return render_template('login.html', error=error, error_msg=error_msg)
        else:
            error = True
            error_msg = 'Email not found'
            return render_template('login.html', error=error, error_msg=error_msg)
    else:
        error = True
        error_msg = 'Email not found'
        db.close()
        return render_template('login.html', error=error, error_msg=error_msg)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signupp', methods=['POST'])
def signupp():
    global mail
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
            db.close()
            error = True
            error_msg = 'Account already exists, pleas login'
            return render_template('signup.html', error=error, error_msg=error_msg);
        else:
            cursor.execute("INSERT into members(email, password) VALUES (?, ?)", (mail, password))
            db.commit()
            db.close()
            return render_template('form.html')
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
        return render_template('form.html')


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/register', methods=['POST'])
def register():
    # do something
    #print(g.mail)
    global mail
    db = sqlite3.connect('temp.db')
    name = request.form['name']
    image = request.form['image']
    branch = request.form['branch']
    cg = request.form['cg']
    gender = request.form.get('gender')
    age = request.form['age']
    sleeptime = request.form.get('sleeptime')
    wakeup = request.form.get('wakeup')
    organised = request.form.get('organised')
    social = request.form.get('social')
    noise = request.form.get('noise')
    smoke = request.form.get('smoke')
    medications = request.form.get('medications')
    cg_p = request.form['cg_p']
    cg_p_max = request.form['cg_p_max']
    branch_p = request.form['branch_p']
    smoke_p = request.form.get('smoke_p')

    cursor = db.cursor()
    try:
        cursor.execute('''CREATE TABLE details(email varchar(100) PRIMARY KEY,name varchar(100),image varchar(100),branch varchar(100),cg INTEGER,gender varchar(100),age varchar(100),sleeptime varchar(100),wakeup varchar(100),organised INTEGER,social varchar(100),noise varchar(100),smoke varchar(100),medications varchar(100),cg_p INTEGER,cg_p_max INTEGER,branch_p varchar(100),smoke_p varchar(100))''')
    # # db.close()
    # # db = sqlite3.connect('temp.db')
    except sqlite3.OperationalError:
        # Table already exists
        pass
    # cursor = db.cursor()
    cursor.execute(
        "INSERT into details(email,name,image,branch,cg,gender,age,sleeptime,wakeup,organised,social,noise,smoke,medications,cg_p,cg_p_max,branch_p,smoke_p) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (mail, name,image,branch,cg,gender,age,sleeptime,wakeup,organised,social,noise,smoke,medications,cg_p,cg_p_max,branch_p,smoke_p))
    db.commit()
    db.close()
    return "Succesfully submitted"

@app.route('/results')
def results():

    
    global mail
    db = sqlite3.connect('temp.db')
    cursor = db.cursor()
    print(mail)
    cursor.execute("SELECT gender FROM details WHERE email=?", (mail,))
    gender = cursor.fetchone()[0]
    cursor.execute("SELECT smoke_p FROM details WHERE smoke_p")
    smoke_p = cursor.fetchone()[0]
    # print(gender)
    cursor.execute("SELECT * FROM details WHERE gender=? AND smoke_p=?", (gender,smoke_p))

    rows = cursor.fetchall()
    db.close()
    return render_template('results.html', rows=rows)
if __name__ == "__main__":
    app.run(debug=True)

