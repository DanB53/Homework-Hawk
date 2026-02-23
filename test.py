from flask import Flask, render_template, request, jsonify, abort, session, url_for, redirect
import requests
import time as t
import json
from encryption import encrypt
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"




def logResult(name, response):
    if response.status_code == 200:
        print(name,"Success")
    else:
        print(name,"Error")

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # print(request.form["button-clicked"])
        if request.form["button-clicked"] == "fake-login":
            url = "http://127.0.0.1:5000/login"
            name = encrypt(5486416585555566,"a")
            payload = {"login_details":[name,"",""]}
            try:
                x = requests.post(url,json=payload)
            except ConnectionError:
                return "Server not up."
            logResult("Correct Username",x)
            payload = {"login_details":[name,"",""]}
            x = requests.delete(url)
            logResult("Incorrect Method",x)
    return render_template('tests.html')



if __name__ == '__main__':
    app.run(debug=True, port=5001)
