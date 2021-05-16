import sys
import os

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
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
            newname = core.transfer_uploads_to_storage().split('\\')[-1]
            flash(f"File uploaded: {newname}")
            return redirect(url_for("upload_file"))

    types = core.load_types()
    categories = core.load_categories()
    # TODO update with current month
    default_date = "2021-03"
    return render_template("uploader.html", types=types, categories=categories, default_date=default_date)


@app.route("/types", methods=["GET"])
def type_management():
    fields = core.load_types()
    return render_template("types.html", fields=fields)


@app.route("/categories", methods=["GET"])
def category_management():
    fields = core.load_categories()
    return render_template("categories.html", fields=fields)


@app.route("/types/delete/<name>", methods=["GET"])
def type_delete(name):
    interface = core.get_type_interface()
    interface.delete(name)
    flash(f"deleted type: {name}")
    return redirect(url_for("type_management"))


@app.route("/categories/delete/<name>", methods=["GET"])
def category_delete(name):
    interface = core.get_category_interface()
    interface.delete(name)
    flash(f"deleted category: {name}")
    return redirect(url_for("category_management"))


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/categories/create", methods=["GET"])
def create_category():
    name = request.args.get("name", "")
    if name != "":
        message = core.create_category(name)
        flash(message)
    return redirect(url_for("category_management"))


@app.route("/types/create", methods=["GET"])
def create_type():
    name = request.args.get("name", "")
    if name != "":
        message = core.create_type(name)
        flash(message)
    return redirect(url_for("type_management"))


@app.route("/files", methods=["GET"])
def list_files():
    files = core.load_details_of_all_files()
    return render_template("files.html", files=files)
