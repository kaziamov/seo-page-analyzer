from flask import Flask, render_template, request, redirect, url_for
# import psycopg2
# from dotenv import load_dotenv
from urllib.parse import urlparse


app = Flask(__name__)

title = "Page Analyzer"


def is_valid(data):
    checker = urlparse(data)
    return all([checker.scheme, checker.netloc, checker.path, len(data) < 255])


@app.get("/")
def root():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template("home.html", title=title)


@app.route("/url/<int:id>")
def get_url(id):
    return render_template("index.html", title=title)


@app.route("/invalid_url")
def invalid_url():
    return render_template("invalid_url.html", title=title)


@app.route("/add_new_url", methods=["POST"])
def add_new_url():
    url = request.form.get("url")
    if is_valid(url):
        print(f'URL {url} is OK')
        return redirect(url_for('urls'))
    else:
        print(f'URL {url} not OK :(')
        return redirect(url_for('invalid_url'))


@app.route("/urls")
def urls():
    return render_template("urls.html", title=title)


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404


if __name__ == '__main__':
    app()
