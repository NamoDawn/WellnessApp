#!/usr/bin/python3
<<<<<<< HEAD
from flask import Flask, render_template, jsonify, request
import pymysql
from flask_cors import CORS, cross_origin
import json
import uuid

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', strict_slashes=False)
def mainpage():
    return render_template('login.html',
                           cache_id=uuid.uuid4())

#@app.route('/serve/', strict_slashes=False)
#def serve():
#    """ renders index.html template """
#    results = []
#    return render_template('index.html',
#                           results=results)


@app.route('/sign_up/', methods=['GET', 'OPTIONS', 'POST'], strict_slashes=False)
def sign_up():
    """ inserts new user credentials into 'credentials' table """
    response = request.data.decode('utf-8')
    obj = json.loads(response)

    con = pymysql.connect('localhost', 'root', 'adminroot', 'wellness_dev_db')
    cursor = con.cursor()
    email = obj[0]['email']
    password = obj[0]['password']
    cursor.execute("INSERT INTO credentials (email, password, f_name, l_name) VALUES('{}', '{}', '{}', '{}')".format(email, password, obj[0]['f_name'], obj[0]['l_name']))
    con.commit()
    con.close()
    if user_exists(email):
        return jsonify(True)
    return jsonify(False)

def user_exists(email, password=None):
    """ confirms existance of email in 'credentials table', w. option to validate email  """
    con = pymysql.connect('localhost', 'root', 'adminroot', 'wellness_dev_db')
    cursor = con.cursor()
    results = ()
    if password:
        cursor.execute("SELECT * FROM credentials WHERE email='{}' AND password='{}'".format(email, password))
        results = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM credentials WHERE email='{}'".format(email))
        results = cursor.fetchall()
    if results == (()):
        return False
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
