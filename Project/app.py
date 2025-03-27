from flask import Flask, render_template, request, redirect, session
import secrets

import pandas as pd


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return render_template('Home.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)





