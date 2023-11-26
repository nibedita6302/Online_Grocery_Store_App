from flask import request, session, render_template, url_for, redirect
from flask import current_app as app
from ..api.inventory import *
from ..api.users import *

@app.get("/")
def Home():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def LoginPage():
    return {}

