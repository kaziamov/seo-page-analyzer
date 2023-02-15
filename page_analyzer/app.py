from flask import Flask, render_template, request, jsonify
import psycopg2
from dotenv import load_dotenv



app = Flask(__name__)


def is_valid(data):
    checks = [
        len(data['url']) < 255,
        data['url'][0:7] == 'https://' or data['url'][0:6] == 'http://',
        ]
    return all(checks)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/url/<int:id>")
def get_url(id):
    # url = request.args.get('url')
    # if is_valid(url):
    #     error = None
    return render_template("index.html")


@app.route("/urls")
def get_urls():
    # url = request.args.get('url')
    # if is_valid(url
    #     error = None
    return render_template("index.html")


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404


if __name__ == '__main__':
    app()
