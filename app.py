from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')

mail=""

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
    print("YES")
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
        cursor.execute('''CREATE TABLE details(email varchar(100) PRIMARY KEY,name varchar(100),image varchar(100),branch varchar(100),cg FLOAT(4, 2),gender varchar(100),age varchar(100),sleeptime varchar(100),wakeup varchar(100),organised INTEGER,social varchar(100),noise varchar(100),smoke varchar(100),medications varchar(100),cg_p FLOAT(4, 2),cg_p_max FLOAT(4, 2),branch_p varchar(100),smoke_p varchar(100))''')
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
    return redirect(url_for('results'))

@app.route('/results')
def results():
    global mail
    db = sqlite3.connect('temp.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM details")
    res = cursor.fetchall()
    cursor.execute("SELECT * FROM details WHERE email =?", (mail,))
    rowdata = cursor.fetchall()
    lst = []
    for row in res:
        if(row[0] == mail):
            continue
        if(row[5] != rowdata[0][5]):
            continue
        percent = 0
        if float(row[4]) >= float(rowdata[0][14]) and float(row[4]) <= float(rowdata[0][15]):
            percent += 20
        else:
            if float(row[4]) > float(rowdata[0][15]):
                diff = float(row[4]) - float(rowdata[0][15])
            else:
                diff = float(rowdata[0][14]) - float(row[4])
            percent += 20 - 3*float(diff)
        per2 = str(row[7])
        per1 = str(rowdata[0][7])
        if(per1[0] == 'A'):
            x = 16
        elif(per1[2] == 'A'):
            x = 12
        elif(per1[1] == 'A'):
            x = 13
        elif(per1[1] == 'P'):
            x = int(per1[0])
        elif(per1[2] == 'P'):
            x = int(per1[0])*10 + int(per1[1])
        if(per2[0] == 'A'):
            y = 18
        elif(per2[2] == 'A'):
            y = 12
        elif(per2[1] == 'A'):
            y = 13
        elif(per2[1] == 'P'):
            y = int(per2[0])
        elif(per2[2] == 'P'):
            y = int(per2[0])*10 + int(per2[1])
        percent += 20 - 3*abs(x - y)
        per2 = str(row[8])
        per1 = str(rowdata[0][8])
        if(per1[0] != 'A'):
            x = int(per1[0])
        else:
            x = 11
        if(per2[0] != 'A'):
            y = int(per2[0])
        else:
            y = 9
        percent += 20 - 3*abs(x - y)
        per2 = str(row[12])
        per1 = str(rowdata[0][17])
        if(per2 == per1):
            percent += 20
        else:
            percent += 5
        per2 = str(row[10])
        per1 = str(rowdata[0][11])
        if(per1[0] == 'C' and per2[0] == 'S'):
            percent += 10
        elif(per1[0] == 'C' and per2[0] == 'N'):
            percent += 5
        if(per1[0] == 'N' and per2[0] == 'N'):
            percent += 10
        elif(per1[0] == 'N' and per2[0] == 'S'):
            percent += 5
        per1 = str(rowdata[0][16])
        per2 = str(row[3])
        if(per1 == per2 or per1 == "Any"):
            percent += 10
        new_tup = (int(percent), ) + row
        lst.append(new_tup)
    sorted_list = sorted(lst, key=lambda x:x[0], reverse=True)
    return render_template('search.html', result=sorted_list[0], current_row = 0)

@app.route('/display', methods=['POST'])
def display():
    global mail
    db = sqlite3.connect('temp.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM details")
    res = cursor.fetchall()
    cursor.execute("SELECT * FROM details WHERE email =?", (mail,))
    
    rowdata = cursor.fetchall()
    lst = []
    for row in res:
        if(row[0] == mail):
            continue
        if(row[5] != rowdata[0][5]):
            continue
        percent = 0
        if float(row[4]) >= float(rowdata[0][14]) and float(row[4]) <= float(rowdata[0][15]):
            percent += 20
        else:
            if float(row[4]) > float(rowdata[0][15]):
                diff = float(row[4]) - float(rowdata[0][15])
            else:
                diff = float(rowdata[0][14]) - float(row[4])
            percent += 20 - 3*float(diff)
        per2 = str(row[7])
        per1 = str(rowdata[0][7])
        if(per1[0] == 'A'):
            x = 16
        elif(per1[2] == 'A'):
            x = 12
        elif(per1[1] == 'A'):
            x = 13
        elif(per1[1] == 'P'):
            x = int(per1[0])
        elif(per1[2] == 'P'):
            x = int(per1[0])*10 + int(per1[1])
        if(per2[0] == 'A'):
            y = 18
        elif(per2[2] == 'A'):
            y = 12
        elif(per2[1] == 'A'):
            y = 13
        elif(per2[1] == 'P'):
            y = int(per2[0])
        elif(per2[2] == 'P'):
            y = int(per2[0])*10 + int(per2[1])
        percent += 20 - 3*abs(x - y)
        per2 = str(row[8])
        per1 = str(rowdata[0][8])
        if(per1[0] != 'A'):
            x = int(per1[0])
        else:
            x = 11
        if(per2[0] != 'A'):
            y = int(per2[0])
        else:
            y = 9
        percent += 20 - 3*abs(x - y)
        per2 = str(row[12])
        per1 = str(rowdata[0][17])
        if(per2 == per1):
            percent += 20
        else:
            percent += 5
        per2 = str(row[10])
        per1 = str(rowdata[0][11])
        if(per1[0] == 'C' and per2[0] == 'S'):
            percent += 10
        elif(per1[0] == 'C' and per2[0] == 'N'):
            percent += 5
        if(per1[0] == 'N' and per2[0] == 'N'):
            percent += 10
        elif(per1[0] == 'N' and per2[0] == 'S'):
            percent += 5
        per1 = str(rowdata[0][16])
        per2 = str(row[3])
        if(per1 == per2 or per1 == "Any"):
            percent += 10
        new_tup = (int(percent), ) + row
        lst.append(new_tup)
    sorted_list = sorted(lst, key=lambda x:x[0], reverse=True)
    total_rows = len(sorted_list)
    current_row = int(request.form.get('current_row', 0))
    if request.method == 'POST':
        button = request.form['button']
        if button == 'next':
            current_row += 1
            if current_row == total_rows:
                current_row = 0
        elif button == 'previous':
            current_row -= 1
            if current_row == -1:
                current_row = total_rows - 1
    return render_template('search.html', result=sorted_list[current_row], current_row=current_row)

if __name__ == "__main__":
    app.run(debug=True)