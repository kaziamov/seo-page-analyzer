from flask import Flask, render_template, request, flash, redirect, url_for
from urllib.parse import urlparse
from datetime import timedelta
from page_analyzer.models import Database
import requests
import bs4

app = Flask(__name__)
app.secret_key = 'test'
app.permanent_session_lifetime = timedelta(hours=24)

d = Database()
title = "Page Analyzer"


def get_data(url):
    try:
        responce = requests.get(url)
    except requests.exceptions.ConnectionError:
        return ()
    return parse_data(responce)


def parse_data(data):
    html = bs4.BeautifulSoup(data.text)
    status = data.status_code
    title = html.title
    h1 = html.find('h1')
    desc = html.find("meta", attrs={'name': 'description'})
    return (status,
            title.string if title else '',
            h1.get_text() if h1 else '',
            desc['content'] if desc else '')


def is_valid(data):
    checker = urlparse(data)
    return all([checker.scheme, checker.netloc, checker.path, len(data) < 255])


@app.route('/')
def home():
    return render_template("home.html", title=title)


@app.route("/urls/<int:id>")
def urls_id(id):
    name = ''
    date = ''
    checks = []
    url_data = d.get_data_by_id(id)
    if url_data:
        name = url_data[1]
        date = url_data[2]
    if d.is_checks_exist(id):
        checks = d.get_checks_by_id(id)
    return render_template("urls_id.html", title=name,
                           name=name, date=date, id=id, checks=checks)


@app.route("/urls/<int:id>/checks", methods=['POST'])
def url_check(id):
    if request.method == 'POST':
        url = d.get_data_by_id(id)[1]
        data = get_data(url)
        if data:
            d.add_new_check(id, *data)
        else:
            flash('Произошла ошибка при проверке')
    return redirect(url_for('urls_id', id=id))


# @app.route("/invalid_url")
# def invalid_url():
#     return render_template("invalid_url.html", title=title)


@app.route("/urls", methods=["GET", "POST"])
def urls():
    if request.method == 'POST':
        url = request.form.get("url")

        if is_valid(url):

            id = d.is_url_exist(url)
            if id is not False:
                flash("Страница уже существует")
                return urls_id(id=id)

            d.add_new_url(url)
            flash("Страница успешно добавлена")
            id = d.is_url_exist(url)
            return urls_id(id=id)

        else:
            flash("Некорректный URL")
            return redirect(url_for('home'))

    else:
        urls = d.get_all_urls()
        print('GET ALL URLS', urls)
        return render_template("urls.html", title=title, urls=urls)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")


if __name__ == '__main__':
    app()
