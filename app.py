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
def load_main_page():
    """
    renders login.html
    Reutn: rendered html
    """
    return render_template('login.html',
                           cache_id=uuid.uuid4())


@app.route('/save_exp/', methods=['POST'],
           strict_slashes=False)
def save_exp():
    """
    inserts new experience into 'experiences' table
    Return: always returns jsonified True
    """
    response = request.data.decode('utf-8')
    obj = json.loads(response)

    con = pymysql.connect('localhost', 'wellness_dev',
                          'wellness_dev_pwd', 'wellness_dev_db')
    cursor = con.cursor()
    exp_name = obj['exp_name']
    scale = obj['scale']
    date = datetime.now().strftime('%Y-%m-%d 00:00:00')
    exp_type = obj['type']
    user_id = obj['user_id']
    count = 0
    dates = []

    if scale == '':
        scale = 5

    cursor.execute('SELECT `count`, `date` \
    FROM `experiences` \
    WHERE exp_name=\'{}\' AND date=\'{}\' \
    ORDER BY date DESC'.format(exp_name, date))

    result = cursor.fetchall()

    if not result:
        count = 1
    else:
        for item in result:
            if date == str(item[1]):
                cursor.execute("UPDATE experiences \
                SET count=count+1 \
                WHERE date='{}'".format(date))

                con.commit()
                con.close()
                return jsonify(True)
            else:
                dates.append(item[1])

    cursor.execute(
        'INSERT INTO experiences (exp_name, scale, date, type, user_id, count) \
        VALUES("{}", "{}", "{}", "{}", "{}", "{}")'.format(
            exp_name, scale, date, exp_type, user_id, count))
    con.commit()
    con.close()

    return jsonify(True)


def data_exists(exp_name, date):
    """
    confirms existance of experience entry in 'experiences table'
    Return: False if 'results' tuple is empty. True otherwise.
    """
    con = pymysql.connect('localhost',
                          'wellness_dev',
                          'wellness_dev_pwd',
                          'wellness_dev_db')
    cursor = con.cursor()
    results = ()
    var1 = cursor.execute("SELECT EXISTS(SELECT 1 \
    FROM experiences \
    WHERE exp_name='{}' AND date='{}')".format(exp_name, date))
    results = cursor.fetchone()
    cursor.execute("SELECT * FROM credentials WHERE email='{}'".format(email))
    results = cursor.fetchall()
    if results == (()):
        return False
    return True


@app.route('/signup/', methods=['POST'], strict_slashes=False)
def signup():
    """
    inserts new user credentials into 'credentials' table
    Return: jsonified 'True' if user exists. False otherwise
    """
    response = request.data.decode('utf-8')
    obj = json.loads(response)
    email = obj[0].get('email')
    password = obj[0].get('password')
    if user_exists(email):
        return jsonify(True)
    con = pymysql.connect('localhost',
                          'wellness_dev',
                          'wellness_dev_pwd',
                          'wellness_dev_db')
    cursor = con.cursor()

    cursor.execute("INSERT INTO credentials (email, password, f_name, l_name) \
    VALUES('{}', '{}', '{}', '{}')".format(email, password,
                                           obj[0].get('f_name'),
                                           obj[0].get('l_name')))
    con.commit()
    con.close()
    if user_exists(email):
        return jsonify(True)
    return jsonify(False)


@app.route('/experience/', strict_slashes=False)
def load_experience_page():
    """
    renders experience.html
    Return: rendered html
    """
    return render_template('experience.html')


@app.route('/signin/', methods=['POST'], strict_slashes=False)
def signin():
    """
    Authorizes a user to enter their member page
    Reuturn: jsonified tuple (<email>, True) on
             success. jsonified False otherwise
    """
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
    """
    Confirms existance of email in 'credentials table',
    w. option to validate email
    Return: value of id column in credentials table
    """
    con = pymysql.connect('localhost',
                          'wellness_dev',
                          'wellness_dev_pwd',
                          'wellness_dev_db')
    cursor = con.cursor()
    results = []
    if password:
        cursor.execute("SELECT * FROM credentials \
        WHERE email='{}' AND password='{}'".format(email, password))
        results = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM credentials \
        WHERE email='{}'".format(email))
        results = cursor.fetchall()
    if results == (()):
        return False
    return results[0]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
