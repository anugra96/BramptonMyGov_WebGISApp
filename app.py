from flask import Flask, render_template, send_from_directory
from random import random
import threading
import time
from make_geojson import make_geojson
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.route("/")
def index():
    return render_template('landing.html')



@app.route("/<code>")
def hello(code):
    # make fancy operations if you want
    make_geojson(code)
    time.sleep(2)


    return render_template('index.html')
    # if (code == "testing"):
    #     return render_template('index2.html')
    # else:
    #     return render_template('./index.html')



if __name__ == "__main__":
    app.run()