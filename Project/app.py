from flask import Flask, render_template, request, redirect, session
from jinja2 import TemplateNotFound
import secrets
from flask import abort


import pandas as pd


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return render_template('home/Home.html')

@app.route('/services')
def services_main():
    return render_template('services/services.html')


@app.route('/services/<animal>')
def services_page(animal):
    try:
        return render_template(f'services/{animal}.html' , animal=animal)
    except TemplateNotFound:
        abort(404)


@app.route('/about')
def about():
    return render_template('about/about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

# @app.route('/<page>')
# def render_page(page):
#     try:
#         return render_template(f"{page}.html")
#     except:
#         abort(404)


if __name__ == "__main__":
    app.run(debug=True)

