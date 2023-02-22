from flask import Flask, render_template, request, flash, redirect, url_for

from datetime import timedelta

from page_analyzer.models import Connection
from page_analyzer.parsing import get_data
from page_analyzer.validation import is_valid


app = Flask(__name__)
app.secret_key = 'test'
app.permanent_session_lifetime = timedelta(hours=24)

conn = Connection()
title = "Page Analyzer"


@app.route('/')
def home():
    return render_template("home.html", title=title)


@app.route("/urls/<int:id>")
def urls_id(id):
    name = ''
    date = ''
    checks = []
    url_data = conn.get_data_by_id(id)
    if url_data:
        name = url_data[1]
        date = url_data[2]
    if conn.is_checks_exist(id):
        checks = conn.get_checks_by_id(id)
    return render_template("urls_id.html", title=name, name=name, date=date, id=id, checks=checks)


@app.route("/urls/<int:id>/checks", methods=['POST'])
def url_check(id):
    if request.method == 'POST':
        url = conn.get_data_by_id(id)[1]
        data = get_data(url)
        if data:
            conn.add_new_check(id, *data)
        else:
            flash('Произошла ошибка при проверке')
    return redirect(url_for('urls_id', id=id))


@app.route("/urls", methods=["GET", "POST"])
def urls():
    if request.method == 'POST':
        url = request.form.get("url")
        if is_valid(url):
            id = conn.is_url_exist(url)
            if id is not False:
                flash("Страница уже существует")
                return urls_id(id=id)
            conn.add_new_url(url)
            flash("Страница успешно добавлена")
            id = conn.is_url_exist(url)
            return urls_id(id=id)
        else:
            flash("Некорректный URL")
            return redirect(url_for('home'))
    else:
        urls = conn.get_all_urls()
        print('GET ALL URLS', urls)
        return render_template("urls.html", title=title, urls=urls)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")


if __name__ == '__main__':
    app()
