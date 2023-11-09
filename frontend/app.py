import requests
from frontend.src.tags import TAGS
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    session,
    flash,
)
import json
from frontend.src.helper import generate_uuid
from frontend.src.helper import generate_uuid
import os
from flask_sse import sse
from flask import Flask, session
from src.google_events.data_fetch import fetch_google_data


app = Flask(__name__, template_folder="./templates", static_folder="./static")

app.config.update(SECRET_KEY=os.urandom(24))

app.config["PERMANENT_SESSION_LIFETIME"] = 86400  # 1 day in seconds
app.register_blueprint(sse, url_prefix="/stream")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        url = "https://202q8mozdg.execute-api.us-east-1.amazonaws.com/dev/users"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        users = response.json()
        user_details = request.form
        user_email = user_details["email"]
        for user in users:
            if user["email"] == user_email:
                session["logged_in"] = True
                session["uid"] = user["id"]
                session["session_name"] = user["name"]
                return redirect(url_for("index"))
        flash("Incorrect Login Credentials", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    url = "https://202q8mozdg.execute-api.us-east-1.amazonaws.com/dev/users"
    if request.method == "POST":
        user_details = request.form
        first_name = user_details["first-name"]
        last_name = user_details["last-name"]
        email = user_details["email"]
        tag1 = user_details["S1"]
        tag2 = user_details["S2"]
        if tag1 == tag2:
            flash("You need to select two distince tags", "danger")
            return render_template("register.html")
        params = {
            "id": str(generate_uuid()),
            "name": first_name + " " + last_name,
            "email": email,
            "tags": tag1 + "," + tag2,
        }
        payload = json.dumps(params)
        headers = {"Content-Type": "text/plain"}
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        flash("You are now registered and can login", "success")
        return redirect(url_for("login"))

    return render_template("register.html", taglist=TAGS)


@app.route("/callback", methods=["GET", "POST"])
def index():
    # print(session)
    # if "uid" not in session:
    #     flash("Please login to continue", "danger")
    #     return redirect(url_for("login"))
    # user_id = session["uid"]
    # if user_id == None:
    #     user_id = "1"
    # cur = mysql.connection.cursor()
    # try:
    #     cur.execute("SELECT * from Category")
    # except Exception as e:
    #     raise Exception(f"UNable to run query. Error: {e}")
    # catlist = cur.fetchall()

    # query = f"select * from VP_Products where Availability='Yes'"
    if request.method == "POST":
        form_details = request.form
        try:
            tag_name = form_details["cat"]
        except:
            tag_name = "0"
        if tag_name != "0":
            flash("The relevant tag information will be notified to you soon")
            fetch_google_data(tag_name)
            return redirect(url_for("index"))

    return render_template("index.html", taglist=TAGS)


if __name__ == "__main__":
    # Adjust the host and port as needed
    app.run()
