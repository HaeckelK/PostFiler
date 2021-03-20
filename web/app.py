import sys
import os

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename

sys.path.insert(0, "../")
import core  # noqa E402


UPLOAD_FOLDER = "../uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

assert app.config["SECRET_KEY"] != ""


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            details = {}
            for arg in ("category", "correspondenceType", "correspondenceDate"):
                details[arg] = request.form[arg]
            core.save_file_and_record_details(file, filename, details=details)
            return redirect(url_for("upload_file"))

    types = ("statement", "policy", "bill")
    categories = core.load_categories()
    default_date = "2021-03"
    return render_template("uploader.html", types=types, categories=categories, default_date=default_date)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/categories/create/<name>", methods=["GET"])
def create_category(name):
    message = core.create_category(name)
    return jsonify(message)
