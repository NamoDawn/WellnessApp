#!/usr/bin/python3
from flask import Flask, render_template, jsonify, request
import pymysql
from flask_cors import CORS, cross_origin
import json
import uuid
from datetime import datetime
import time

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', strict_slashes=False)
def mainpage():
    return render_template('login.html',
                           cache_id=uuid.uuid4()
    )

@app.route('/save_exp/', methods=['GET', 'OPTIONS', 'POST'], strict_slashes=False)
def save_exp():
    """ inserts new experience into 'experiences' table """
    response = request.data.decode('utf-8')
    obj = json.loads(response)

    con = pymysql.connect('localhost', 'wellness_dev', 'wellness_dev_pwd', 'wellness_dev_db')
    cursor = con.cursor()
    exp_name = obj['exp_name']
    scale = obj['scale']
    if scale == '':
        scale = 5
    date = datetime.now().strftime('%Y-%m-%d 00:00:00')
    _type = obj['type']
    user_id = obj['user_id']
    count = 0

    cursor.execute('SELECT `count`, `date` FROM `experiences` WHERE exp_name=\'{}\' AND date=\'{}\' ORDER BY date DESC'.format(exp_name, date))

    result = cursor.fetchall();
    dates = [];

    if not result:
        count = 1
    else:
        for item in result:
            if date == str(item[1]):
                cursor.execute("UPDATE experiences set count=count+1 where date='{}'".format(date))
                con.commit()
                con.close()
                return jsonify(True)
            else:
                dates.append(item[1])

    cursor.execute('INSERT INTO experiences (exp_name, scale, date, type, user_id, count) VALUES("{}", "{}", "{}", "{}", "{}", "{}")'.format(exp_name, scale, date, _type, user_id, count))
    con.commit()
    con.close()

    return jsonify(False)

def data_exists(exp_name, date):
    """ confirms existance of experience entry  in 'experiences table'"""
    con = pymysql.connect('localhost', 'wellness_dev', 'wellness_dev_pwd', 'wellness_dev_db')
    cursor = con.cursor()
    results = ()
    var1 = cursor.execute("SELECT EXISTS(SELECT 1 FROM experiences WHERE exp_name='{}' AND date='{}')".format(exp_name, date))
    print(var1)
    results = cursor.fetchone()
    cursor.execute("SELECT * FROM credentials WHERE email='{}'".format(email))
    results = cursor.fetchall()
    if results == (()):
        return False
    return True

@app.route('/signup/', methods=['GET', 'OPTIONS', 'POST'], strict_slashes=False)
def signup():
    """ inserts new user credentials into 'credentials' table """
    response = request.data.decode('utf-8')
    print('response: {}'.format(response))
    obj = json.loads(response)
    email = obj[0].get('email')
    password = obj[0].get('password')
    if user_exists(email):
        print('This email is already registered')
        return jsonify(True)
    con = pymysql.connect('localhost', 'wellness_dev', 'wellness_dev_pwd', 'wellness_dev_db')
    cursor = con.cursor()

    cursor.execute("INSERT INTO credentials (email, password, f_name, l_name) VALUES('{}', '{}', '{}', '{}')".format(email, password, obj[0].get('f_name'), obj[0].get('l_name')))
    con.commit()
    con.close()
    if user_exists(email):
        print('succesfully created user account for {}'.format(email))
        return jsonify(True)
    print('user creation failed!')
    return jsonify(False)

@app.route('/experience/', strict_slashes=False)
def experience():
    """ renders experience.html  """
    return render_template('experience.html')

@app.route('/signin/', methods=['POST'], strict_slashes=False)
def signin():
    """ Authorizes a user to enter their member page  """
    user_creds = []
    try:
        email = json.loads(request.data.decode('utf-8'))[0].get('email')
        password = json.loads(request.data.decode('utf-8'))[0].get('password')
        user_creds = user_exists(email, password)
    except:
        return jsonify(False)
    if user_creds:
            user_id = user_creds[0]
            return jsonify((user_id, True))
    return jsonify(False)

def user_exists(email, password=None):
    """ confirms existance of email in 'credentials table', w. option to validate email  
    Return: calue of id column in credentials table"""
    con = pymysql.connect('localhost', 'wellness_dev', 'wellness_dev_pwd', 'wellness_dev_db')
    cursor = con.cursor()
    results = []
    if password:
        cursor.execute("SELECT * FROM credentials WHERE email='{}' AND password='{}'".format(email, password))
        results = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM credentials WHERE email='{}'".format(email))
        results = cursor.fetchall()
    if results == (()):
        return False
    return results[0]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
