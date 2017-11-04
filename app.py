#!/usr/bin/python3
import csv
from datetime import datetime
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, jsonify, request, make_response
import json
import os
from passlib.hash import sha256_crypt
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


@app.route('/load_vis/', strict_slashes=False)
def load_vis():
    return render_template('data_vis.html',
                           cache_id=uuid.uuid4())


@app.route('/load_vis/static/data', methods=['GET'], strict_slashes=False)
def static_data():
    """ reads csv file and formats for return to data visualizer  """
    data = ""
    with (open("static/data/everything.csv", newline="")) as f:
        csv = f.read()

    response = make_response(csv)
    cd = 'attachment; filename=mycsv.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype = 'text/csv'

    return response


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

        cursor.gexecute('SELECT `count`, `date`, `type` \
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
                'INSERT INTO experiences \
                (exp_name, scale, date, type, user_id, count) \
                VALUES("{}", "{}", "{}", \
                "{}", "{}", "{}")'.format(exp_name, scale, date,
                                          exp_type, user_id, count))
            con.commit()
    con.close()
    return jsonify(True)


@app.route('/vis/', methods=['POST', 'GET'], strict_slashes=False)
def vis():
    """
    fetches user experience info and returns to front
    in csv format for use with data visualization
    """
    user_id = request.data.decode('utf-8')
    generate_csv_files(user_id)
    return jsonify(True)


def generate_csv_files(user_id):
    """
    creates three csv file (7, 30 and life)
    for use when laoding data visualization
    """
   # 7 days
    experiences = fetch_data(user_id, 7)
    obj = []
    for exp in experiences:
        obj.append({'name': exp[0],
                    'count': exp[1],
                    'type': exp[2],
                    'scale': exp[3]})
    with (open("static/data/week.csv", "w", newline="")) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "count", "type", "scale"])
        for o in obj:
            writer.writerow([o["name"],
                             o["count"],
                             o["type"],
                             o["scale"]])

    # 30 days
    experiences = fetch_data(user_id, 30)

    obj = []
    for exp in experiences:
        obj.append({'name': exp[0],
                    'count': exp[1],
                    'type': exp[2],
                    'scale': exp[3]})
    with (open("static/data/month.csv", "w", newline="")) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "count", "type", "scale"])
        for o in obj:
            writer.writerow([o["name"],
                             o["count"],
                             o["type"],
                             o["scale"]])

    # life-to-date
    experiences = fetch_data(user_id)
    obj = []
    for exp in experiences:
        obj.append({'name': exp[0],
                    'count': exp[1],
                    'type': exp[2],
                    'scale': exp[3]})
    with (open("static/data/everything.csv", "w", newline="")) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "count", "type", "scale"])
        for o in obj:
            writer.writerow([o["name"],
                             o["count"],
                             o["type"],
                             o["scale"]])


def fetch_data(user_id, prior_days=None):
    """ fetches user specific data from 'experience' table  """
    con = connect_db()
    cur = con.cursor()
    if prior_days is not None:
        cur.execute("SELECT exp_name, count, type, scale \
        FROM experiences \
        WHERE user_id={} AND \
        date BETWEEN DATE_SUB(\
        NOW(), INTERVAL {} DAY) \
        AND NOW() ORDER BY date DESC".format(user_id, prior_days))
        result = cur.fetchall()
        con.close()
    else:
        cur.execute("SELECT exp_name, count, type, scale \
        FROM experiences \
        WHERE user_id={} \
        ORDER BY date DESC".format(user_id))
        result = cur.fetchall()
        con.close()
    return result


@app.route('/stinky', strict_slashes=False)
def stinky():
    return render_template('stinky.html')


@app.route('/signup/', methods=['POST'], strict_slashes=False)
def signup():
    """
    inserts new user credentials into 'credentials' table
    Return: jsonified 'True' if user exists. False otherwise
    """
    response = request.data.decode('utf-8')
    obj = json.loads(response)
    email = obj[0].get('email')
    password = sha256_crypt.encrypt(obj[0].get('password'))
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


def user_exists(email, password=None):
    """
    Confirms existance of email in 'credentials table',
    Return: value True if exists, False otherwise
    """
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM credentials \
    WHERE email='{}'".format(email))
    results = cursor.fetchall()
    if results == (()):
        return False
    return True


@app.route('/experience/', strict_slashes=False)
def load_experience_page():
    """
    renders experience.html
    Return: rendered html
    """
    return render_template('experience.html',
                           cache_id=uuid.uuid4())


@app.route('/signin/', methods=['POST'], strict_slashes=False)
def signin():
    """
    Validates user credentials
    Reuturn: tuple of user_id and True if validated, False otherwise
    """
    try:
        email = json.loads(request.data.decode('utf-8'))[0].get('email')
        password = json.loads(request.data.decode('utf-8'))[0].get('password')
        db_creds = fetch_credentials(email)
        db_password = db_creds[2]
        user_id = db_creds[0]
        validated = sha256_crypt.verify(password, db_password)
    except:
        validated = False

    return jsonify((user_id, validated))


def fetch_credentials(email):
    """
    Confirms existance of email in 'credentials table',
    w. option to validate email
    Return: value of id column in credentials table
    """
    con = connect_db()
    cursor = con.cursor()
    results = []
    cursor.execute("SELECT * FROM credentials \
    WHERE email='{}'".format(email))
    results = cursor.fetchall()
    con.close()
    if results == (()):
        return ()
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
