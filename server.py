"""PDBV server"""

from flaregen import flare_tree_as_json_for_asn, tree_data_json
from flaregen import adjacency_data_json, sunburst_ready_json
from flaregen import asn_search, tree_ready_json
from flask import Flask, render_template, request, url_for, redirect
from flask.ext.bower import Bower
from model import connect_to_db
import re


# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
Bower(app) # This provides the /bower url route

@app.route('/')
def index():
    return render_template("base.html")


@app.route('/data/tree/<asn>')
def get_tree_data(asn):
    return tree_data_json(asn)


@app.route('/data/adjacency/<asn>')
def get_adjacency_data(asn):
    return adjacency_data_json(asn)


@app.route('/sunburst')
def sunburst():
    current_asn = 19165
    flare_path = "/data/tree/%s" % current_asn
    return render_template('sunburst.html', flare_path=flare_path)


@app.route('/collapsible_tree')
def collapsible_tree():
    current_asn = request.args.get("asn", 3856)
    flare_base = "/data/tree/"
    return render_template('collapsible_tree.html',
                           current_asn=current_asn, flare_base=flare_base)


@app.route('/search')
def search_function():
    # consumes "search" from base.html form
    # uses search as argument that goes into SQL
    # gets back an asn
    # returns a redirect to collapsible tree with that asn
    search = request.args.get("search")
    p = re.compile("^[0-9]+$")
    if p.match(search):
        return redirect(url_for("collapsible_tree", asn=search))
    else:
        asn = asn_search(search)
        return redirect(url_for("collapsible_tree", asn=asn))


if __name__ == "__main__":
    app.config['SQLALCHEMY_ECHO'] = True
    app.debug = True
    connect_to_db(app)
    app.run()
