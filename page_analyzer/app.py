from flask import Flask, render_template, request, flash, redirect, url_for

from datetime import timedelta

from page_analyzer.models import is_checks_exist, get_data_by_id, get_checks_by_id, get_all_urls, add_new_check, add_new_url, is_url_exist
from page_analyzer.parsing import get_data
from page_analyzer.validation import is_valid
from page_analyzer.db_connect import get_connection


app = Flask(__name__)
app.secret_key = 'test'
app.url_map.strict_slashes = False
app.permanent_session_lifetime = timedelta(hours=24)

title = "Page Analyzer"


@app.route('/')
def home(url='', status=200):
    return render_template("home.html", title=title, url=url), status


@app.route("/urls/<int:id>")
def urls_id(id, status=200):
    name = ''
    date = ''
    checks = []
    with get_connection() as conn:
        url_data = get_data_by_id(conn, id)
        if url_data:
            name = url_data[1]
            date = url_data[2]
        if is_checks_exist(conn, id):
            checks = get_checks_by_id(conn, id)
    return render_template("urls_id.html", title=name, name=name, date=date, id=id, checks=checks), status


@app.route("/urls/<int:id>/checks", methods=['POST'])
def url_check(id):
    with get_connection() as conn:
        if request.method == 'POST':
            url = get_data_by_id(conn, id)[1]
            data = get_data(url)
            if data:
                add_new_check(conn, (id, *data))
                flash('Страница успешно проверена', 'success')
                status = 200
            else:
                flash('Произошла ошибка при проверке', 'danger')
                status = 422
        return redirect(url_for('urls_id', id=id, status=status))


@app.route("/urls", methods=["GET", "POST"])
def urls():
    with get_connection() as conn:
        if request.method == 'POST':
            url = request.form.get("url").strip()
            if is_valid(url):
                id = is_url_exist(conn, url)
                if id is not False:
                    flash("Страница уже существует", 'primary')
                else:
                    add_new_url(conn, url)
                    flash("Страница успешно добавлена", 'success')
                    id = is_url_exist(conn, url)
                return redirect(url_for('urls_id', id=id))

            flash("Некорректный URL", 'danger')
            return render_template("home.html", title=title, url=url), 422

        else:
            urls = get_all_urls(conn)
            return render_template("urls.html", title=title, urls=urls)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")


if __name__ == '__main__':
    app()
