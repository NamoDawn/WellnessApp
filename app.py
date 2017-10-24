#!/usr/bin/python3
from datetime import datetime
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, jsonify, request
import json
import os
import pymysql
import time
import uuid

api_host = os.getenv('WELLNESS_API_HOST')
api_port = os.getenv('WELLNESS_API_PORT')
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
user = os.getenv('WELLNESS_MYSQL_USER')
password = os.getenv('WELLNESS_MYSQL_PWD')
host = os.getenv('WELLNESS_MYSQL_HOST')
db = os.getenv('WELLNESS_MYSQL_DB')


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
    objects = json.loads(response)

    con = connect_db()
    cursor = con.cursor()

    for obj in objects:
        exp_name = obj['exp_name']
        scale = obj['scale']
        date = datetime.now().strftime('%Y-%m-%d 00:00:00')
        exp_type = obj['type']
        user_id = obj['user_id']
        count = 0
        dates = []
        is_dupe = False

        if scale == '':
            scale = 5

        cursor.execute('SELECT `count`, `date`, `type` \
        FROM `experiences` \
        WHERE exp_name=\'{}\' AND date=\'{}\' \
        ORDER BY date DESC'.format(exp_name, date))
        result = cursor.fetchall()
        if not result:
            count = 1
        else:
            for item in result:
                if exp_type == str(item[2]) and date == str(item[1]):
                    cursor.execute("UPDATE experiences \
                    SET count=count+1 \
                    WHERE exp_name='{}' AND date='{}'".format(exp_name, date))
                    cursor.execute("SELECT `scale`, `count` \
                    FROM experiences \
                    WHERE exp_name='{}' \
                    AND date LIKE '{}%'".format(exp_name, date))
                    result = cursor.fetchall()[0]
                    db_scale = int(result[0])
                    db_count = int(result[1])
                    avg = ((db_scale) + int(scale)) / db_count

                    cursor.execute("UPDATE experiences \
                    SET scale={} \
                    WHERE exp_name='{}' \
                    AND date='{}'".format(avg, exp_name, date))
                    is_dupe = True
                    con.commit()
                else:
                    dates.append(item[1])

        if is_dupe is False:
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
    con = connect_db()

    cursor = con.cursor()
    results = ()
    var1 = cursor.execute("SELECT EXISTS(SELECT 1 \
    FROM experiences \
    WHERE exp_name='{}' AND date='{}')".format(exp_name, date))
    results = cursor.fetone()
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
    con = connect_db()
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
    con = connect_db()
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


def connect_db():
    """
    makes connection to mysql db, wellness_dev_db
    Return: an open connection to the db
    """
    con = pymysql.connect(host=host,
                          user=user,
                          password=password,
                          db=db)

    return con


if __name__ == '__main__':
    app.run(host=api_host, port=api_port)
