#!/usr/bin/python3
from flask import Flask, render_template, jsonify, request
import pymysql
from flask_cors import CORS, cross_origin
import json
import uuid

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', strict_slashes=False)
def mainpage():
    # TODO: create a landing page. indecx.html should be landing, not login.html
    return render_template('login.html',
                           cache_id=uuid.uuid4()
    )

@app.route('/signup/', methods=['GET', 'OPTIONS', 'POST'], strict_slashes=False)
def signup():
    """ inserts new user credentials into 'credentials' table """
    response = request.data.decode('utf-8')
    print('response: {}'.format(response))
    obj = json.loads(response)
    email = obj[0]['email']
    password = obj[0]['password']
    if user_exists(email):
        print('This email is already registered')
        return jsonify(True)
    con = pymysql.connect('localhost', 'wellness_dev', 'wellness_dev_pwd', 'wellness_dev_db')
    cursor = con.cursor()

    cursor.execute("INSERT INTO credentials (email, password, f_name, l_name) VALUES('{}', '{}', '{}', '{}')".format(email, password, obj[0]['f_name'], obj[0]['l_name']))
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
    email = json.loads(request.data.decode('utf-8'))[0]['email']
    password = json.loads(request.data.decode('utf-8'))[0]['password']
    if user_exists(email, password):
        return jsonify(True)
    return jsonify(False)

def user_exists(email, password=None):
    """ confirms existance of email in 'credentials table', w. option to validate email  """
    con = pymysql.connect('localhost', 'wellness_dev', 'wellness_dev_pwd', 'wellness_dev_db')
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
