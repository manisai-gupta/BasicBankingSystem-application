from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__, static_url_path='', static_folder='templates/')
CORS(app)

conn = sqlite3.connect('bankdatabase.db')
c = conn.cursor()
# c.execute('''CREATE TABLE customers
#                 (sno INTEGER ,name TEXT ,email TEXT UNIQUE,transactionid INTEGER   PRIMARY KEY ,current REAL)''')

# c.execute('''CREATE TABLE transferhistorys
#                 (yourid INTEGER  , othersid INTEGER , amount real)''')
#c.execute('DROP TABLE transferhistorys')
# conn.commit()
# conn.close()


# @app.route('/check')
# def check():
#    conn = sqlite3.connect('bankdatabase.db')
#    c = conn.cursor()
#    c.execute("PRAGMA table_info([customers])")
#    sq = c.fetchall()
#    print(sq)
#    conn.commit()
#    conn.close()
#    return str(sq)


@app.route('/insertdb/')
def insert():
    conn = sqlite3.connect('bankdatabase.db')
    c = conn.cursor()
    records = [(1, 'mani', 'mani@gmail.com', 101, 100),
               (2, 'Elliot', 'elliot@gmail.com', 102, 566),
               (3, 'Bob', 'bob@gmail.com', 103, 1500),
               (4, 'mary', 'mary@gmail.com', 104, 2500),
               (5, 'jenny', 'jenny@gmail.com', 105, 3500),
               (6, 'david', 'david@gmail.com', 106, 4500),
               (7, 'kane', 'kane@gmail.com', 107, 5500),
               (8, 'jane', 'jane@gmail.com', 108, 6500),
               (9, 'chandler', 'chandler@gmail.com', 109, 5500),
               (10, 'joey', 'joey@gmail.com', 110, 9500)]
    c.executemany('INSERT INTO customers VALUES (?,?,?,?,?);', records)

    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/')
def gettodos():
    conn = sqlite3.connect('bankdatabase.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    allcustomer = c.fetchall()
    # print(allcustomer)
    conn.commit()
    conn.close()
    return render_template('index.html', allcustomer=allcustomer)


@app.route('/view/<int:sno>')
def viewcust(sno):
    conn = sqlite3.connect('bankdatabase.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE sno=" + str(sno))
    cust = c.fetchall()
    # print(cust)
    conn.commit()
    conn.close()
    return render_template('view.html', cust=cust)


@app.route('/inputinfo/<int:sno>', methods=['GET'])
def inputid(sno):
    conn = sqlite3.connect('bankdatabase.db')
    c = conn.cursor()
    c.execute("SELECT transactionid FROM customers WHERE sno=" + str(sno))
    data = c.fetchone()
    if data:
        tid = data[0]
    # print(tid)
    conn.commit()
    conn.close()
    return render_template('transfer.html', tid=tid)


@app.route('/inputinfo/', methods=['POST'])
def inputblock():
    if request.method == 'POST':
        ytid = request.form['ytid']
        tid = request.form['tid']
        amount = request.form['Am']
        # print(amount)
        conn = sqlite3.connect('bankdatabase.db')
        c = conn.cursor()
        c.execute('INSERT  INTO transferhistorys VALUES (?,?,?);',
                  (ytid, tid, amount))
        c.execute("SELECT current FROM customers WHERE transactionid ="+ytid)
        s1 = c.fetchall()
        # print(s1)
        todo_array = []
        for t in s1:
            todo_array.append(t)
        l = json.dumps(todo_array[0])
        res = int(float(l[1:-2]))
        val = int(res)-int(amount)
        # print(val)
        c.execute("SELECT current FROM customers WHERE transactionid ="+tid)
        s2 = c.fetchall()
        # print(s2)
        todo_array1 = []
        for t in s2:
            todo_array1.append(t)
        l1 = json.dumps(todo_array1[0])
        # print(l1)
        res1 = int(float(l1[1:-2]))

        val1 = int(res1)+int(amount)
        # print(val1)

        c.execute("UPDATE customers SET CURRENT=" +
                  str(val) + " WHERE transactionid="+str(ytid))

        c.execute("UPDATE customers SET CURRENT=" +
                  str(val1) + " WHERE transactionid="+str(tid))
        conn.commit()
        conn.close()
        return redirect('/')


@app.route('/history/<int:sno>')
def thistory(sno):
    conn = sqlite3.connect('bankdatabase.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE sno=" + str(sno))
    cust = c.fetchall()
    c.execute(
        " SELECT * FROM transferhistorys WHERE yourid in (SELECT transactionid FROM customers WHERE sno= " + str(sno)+")")
    hist = c.fetchall()
    # print(cust)
    # print(hist)
    conn.commit()
    conn.close()
    return render_template('history.html', cust=cust, hist=hist)


if __name__ == "__main__":
    app.run(debug=True)
