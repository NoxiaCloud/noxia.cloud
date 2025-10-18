from flask import Flask, render_template, request, jsonify
from flask_minify import Minify
from werkzeug.exceptions import HTTPException
import logging
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
Minify(app=app, html=True, js=True, cssless=True, static=True)


@app.errorhandler(Exception)
def handle_errors(e):
    if isinstance(e, HTTPException):
        code = e.code
        title = e.name
        message = e.description
    else:
        logging.error(f"Unhandled Exception: {e}", exc_info=True)
        code = 500
        title = "Server Error"
        message = "An unexpected error occurred on the server."

    ref = request.referrer or "/"
    return (
        render_template(
            "errors/index.html",
            title=title,
            code=code,
            message=message,
            ref=ref,
        ),
        code,
    )


@app.route("/")
def index():
    return render_template("/pages/index.html")


@app.route("/api/status")
def status():
    url = "https://status.noxia.cloud/badge?theme=light"
    r = requests.get(url)
    html = r.text

    soup = BeautifulSoup(html, "html.parser")
    status_div = soup.find("div", class_="font-medium")
    status_text = status_div.get_text(strip=True) if status_div else "Unknown"

    return jsonify({"status": status_text})


app.run(host="127.0.0.1", port=5000, debug=True)
