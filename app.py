#!/usr/bin/python3
from flask import Flask, render_template
import uuid

application = Flask(__name__)

@application.route("/")
def mainpage():
    return render_template('experience.html',
                           cache_id=uuid.uuid4())

if __name__ == "__main__":
    application.run(host='0.0.0.0')
