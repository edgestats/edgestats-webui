import json
import os
import requests

from datetime import datetime, timedelta

from flask import Flask, abort, render_template, request, redirect, url_for, session, Response
from flask_wtf import CSRFProtect

from .forms import *
from .helpers import *

from .error import bp_error

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("APPSECRET_KEY", "app secret key")
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)

csrf = CSRFProtect(app)


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchAddress()
    if request.method == "POST" and form.validate_on_submit():
        addr = form.addr.data.strip()
        return redirect(url_for("stats", address=addr))

    return render_template("index.html", form=form)


@app.route("/stats", methods=["GET"])
def stats():
    addr = request.args.get("address").lower()

    # get uptime stats
    min = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    uri = os.getenv("EDGESTATS_API_ADDR") + f"/stats/uptimes/broadcasts/{addr}/{min}"
    headers = {"x-api-key": os.getenv("EDGESTATS_API_KEY")}
    req = requests.request("GET", uri, json={}, headers=headers)

    try:
        statistics = req.json()
    except Exception:
        abort(404, "node address not found")

    # set row ok_status glow colors
    statistics = get_ok_status(statistics)

    # get uptimes & block misses
    aggregates = get_block_uptimes(addr, min)

    # get refresh timestamp
    refreshed_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # get node account stats
    account = get_account_stats(addr=addr)

    # get node stakes by account
    stakes = get_node_stake_by_acc(addr=addr)

    return render_template(
        "stats.html",
        account=account,
        stakes=stakes,
        statistics=statistics, 
        aggregates=aggregates, 
        refreshed_at=refreshed_at
    )


@app.route("/clusters", methods=["GET", "POST"])
def clusters():
    form = SearchClusterAddresses()
    if request.method == "POST" and form.validate_on_submit():
        addrs = form.addrs.data.strip()
        return redirect(url_for("clusters_view", addresses=addrs))

    return render_template("clusters.html", form=form)


@app.route("/clusters/view", methods=["GET"])
def clusters_view():
    addrs = request.args.get("addresses").lower()
    uri = os.getenv("EDGESTATS_API_ADDR") + f"/clusters/uptimes/broadcasts/{addrs}"
    headers = {"x-api-key": os.getenv("EDGESTATS_API_KEY")}
    req = requests.request("GET", uri, json={}, headers=headers)

    try:
        statistics = req.json()
    except Exception:
        abort(404, "node addresses not found")

    # set row ok_status glow colors
    statistics = get_ok_status(statistics)

    # get refresh timestamp
    refreshed_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    return render_template("clusters_view.html", statistics=statistics, refreshed_at=refreshed_at)


@app.route("/nfts", methods=["GET"])
def nfts():
    return render_template("nfts.html")


@app.route("/faqs", methods=["GET"])
def faqs():
    return render_template("faqs.html")


@app.route("/downloads", methods=["GET"])
def downloads():
    return render_template("downloads.html")


app.register_blueprint(bp_error)

if __name__ == "__main__":
    app.run()
