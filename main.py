from dotenv import dotenv_values
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from flask import Flask, render_template, redirect, url_for, request
import json
from random import choice
import os
from tinydb import TinyDB, Query
import shortuuid
db = TinyDB("db.json")


env_config = dotenv_values(".env")

app = Flask(__name__)

app.secret_key = b"random bytes representing flask secret key"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["DISCORD_CLIENT_ID"] = env_config["DISCORD_CLIENT_ID"]
app.config["DISCORD_CLIENT_SECRET"] = env_config["DISCORD_CLIENT_SECRET"]
app.config["DISCORD_REDIRECT_URI"] = env_config["ROOT_URL"] + "/callback"
root = env_config["ROOT_URL"]
discord = DiscordOAuth2Session(app)


def genid():
    return shortuuid.uuid(name=root)


@app.route("/static/<path:path>/")
def static_dir(path):
    return send_from_directory("static", path)


@app.route('/')
def home():
    return render_template("home.html")

@app.route("/login/")
def login():
    return discord.create_session()


@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for("dashboard"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    discord.revoke()
    return redirect(url_for("home"), code=302)


@app.route("/dashboard/")
@requires_authorization
def dashboard():
    return render_template("dashboard.html", user=discord.fetch_user())


@app.route("/api/shorten/", methods=['POST'])
@requires_authorization
def api_shorten():
    r = request.form
    user = discord.fetch_user()
    d = {}
    d["id"] = genid()
    d["shortened_url"] = root + "/u/" + d["id"]
    urlf = r["url"]
    if not urlf.startswith("http://") or urlf.startswith("https://"):
        urlf = "http://" + urlf
    d["original_url"] = urlf
    d["creator_id"] = user.id
    db.insert(d)
    return redirect(root + "/dashboard/success?url=" + d["shortened_url"], code=302)


@app.route("/dashboard/success/")
def shorten_success():
    return render_template("shorten_success.html")


@app.route("/dashboard/urls/")
@requires_authorization
def urls():
    return render_template("urls.html", l=db.all())


@app.route("/api/deleteShorten/")
@app.errorhandler(401)
@requires_authorization
def api_deleteShorten():
    user = discord.fetch_user()
    r = Query()
    if user.id != db.get(r.id == request.args["id"])["creator_id"]:
        return 401
    else:
        p = db.get(r.id == request.args["id"])
        id = p.doc_id
        db.remove(doc_ids=[id])
        return redirect(root + "/dashboard/urls", code=302)


@app.route('/u/<id>/')
def shorten_manager(id):
    r = Query()
    return redirect(db.get(r.id == id)["original_url"], code=302)


if __name__ == "__main__":
    app.run()
