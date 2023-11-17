import requests
from frontend.utils.tags import TAGS
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
from frontend.utils.helper import generate_uuid
from frontend.utils.helper import generate_uuid
import os
from flask_sse import sse
from flask import Flask, session
from src.google_events.data_fetch import fetch_google_data
from src.notifications.notify_user import send_mail

SENDER_MAIL = os.environ.get("SENDER_MAIL")

CREATE_USER_URL = os.getenv("CREATE_USER_URL")
GET_USERS = os.getenv("GET_USERS")


app = Flask(
    __name__, template_folder="./frontend/templates", static_folder="./frontend/static"
)

app.config.update(SECRET_KEY=os.urandom(24))

app.config["PERMANENT_SESSION_LIFETIME"] = 86400  # 1 day in seconds
app.register_blueprint(sse, url_prefix="/stream")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        url = GET_USERS
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
                session["email"] = user["email"]
                return redirect(url_for("index"))
        flash("Incorrect Login Credentials", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    url = CREATE_USER_URL
    if request.method == "POST":
        user_details = request.form
        first_name = user_details["first-name"]
        last_name = user_details["last-name"]
        email = user_details["email"]
        tags = request.form.getlist("tags")
        # tag2 = user_details["S2"]
        # if tag1 == tag2:
        #     flash("You need to select two distince tags", "danger")
        #     return render_template("register.html")
        tags_to_str = ""
        for tag in tags:
            tags_to_str += tag + ","
        params = {
            "id": str(generate_uuid()),
            "name": first_name + " " + last_name,
            "email": email,
            "tags": tags_to_str,
        }
        payload = json.dumps(params)
        headers = {"Content-Type": "text/plain"}
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        flash("You are now registered and can login", "success")
        return redirect(url_for("login"))

    return render_template("register.html", taglist=TAGS)


@app.route("/index", methods=["GET", "POST"])
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
            user_email = session["email"]
            fetch_google_data(tag_name, user_email)
            flash("The relevant tag information has been stored to our database")
            user_email = session["email"]
            sender = SENDER_MAIL
            try:
                send_mail(sender, "Test Mail", [user_email])
                flash(f"Email sent successfully! to {user_email}")
            except Exception as e:
                flash("Error sending email: {response.status_code} - {response.text}")
                print(e)
            return redirect(url_for("index"))

    return render_template("index.html", taglist=TAGS)


if __name__ == "__main__":
    # Adjust the host and port as needed
    app.run()
