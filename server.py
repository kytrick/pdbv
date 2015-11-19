"""PDBV server"""
from flaregen import *
from flask import Flask, render_template, request
from model import connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("base.html")

# Let's start to build some functions

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


@app.route('/rtt/<asn>')
def rtt(asn):
    asn = asn
    flare_path = "/data/tree/%s" % asn
    return render_template('rtt.html', flare_path=flare_path)

# @app.route('/rtt')
# def rtt():
#     current_asn = 19165
#     flare_path = "/data/tree/%s" % current_asn
#     return render_template('rtt.html', flare_path=flare_path)


@app.route('/collapsible_tree')
def collapsible_tree():
    search = request.args.get("search", 3856)
    current_asn = search
    print "CURRENT ASN", current_asn
    # current_asn = 3856
    flare_base = "/data/tree/"
    return render_template('collapsible_tree.html',
                           current_asn=current_asn, flare_base=flare_base)

# @app.route('/collapsible_tree')
# def collapsible_tree():
#     current_asn = 3856
#     flare_path = "/data/tree/%s" % current_asn
#     return render_template('collapsible_tree.html', flare_path=flare_path)


@app.route('/search')
def asn_search(user_input):
    user_input = user_input
    return 

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run()
