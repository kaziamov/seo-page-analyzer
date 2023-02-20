from flask import Flask, render_template, request, flash, redirect, url_for
# import psycopg2
# from dotenv import load_dotenv
from urllib.parse import urlparse
from datetime import timedelta, datetime
from page_analyzer.models import Database


app = Flask(__name__)
app.secret_key = 'test'
app.permanent_session_lifetime = timedelta(hours=24)

d = Database()
title = "Page Analyzer"


def is_valid(data):
    checker = urlparse(data)
    return all([checker.scheme, checker.netloc, checker.path, len(data) < 255])


@app.route('/')
def home():
    return render_template("home.html", title=title)


@app.route("/urls/<int:id>")
def urls_id(id):
    id_, name, date = d.get_data("""SELECT * FROM urls WHERE id='{}'""".format(id))
    return render_template("urls_id.html", title=name,
                           name=name, date=date, id=id)


@app.route("/invalid_url")
def invalid_url():
    return render_template("invalid_url.html", title=title)


@app.route("/urls", methods=["GET", "POST"])
def urls():
    if request.method == 'POST':
        url = request.form.get("url")
        if is_valid(url):
            id = d.is_url_exist(url)
            if id != False:
                flash("Страница уже существует")
                return urls_id(id=id)
            d.add_new_url()
            flash("Страница успешно добавлена")
            id = d.get_data("""SELECT id FROM urls WHERE name='{}'""".format(url))[0]
            return urls_id(id=id)
        else:
            flash("Некорректный URL")
            return redirect(url_for('home'))
    else:
        urls = d.get_all_urls()
        return render_template("urls.html", title=title, urls=urls)


def get_flash(text):
    messages = {
        "check_failed": "Произошла ошибка при проверке",
        "check_success": "Страница успешно проверена"
        }

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")


if __name__ == '__main__':
    app()
