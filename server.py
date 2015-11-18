"""PDBV server"""
from flaregen import *
from flask import Flask, render_template
from model import connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)


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
    return render_template('rrtt.html', flare_path=flare_path)

# @app.route('/rtt')
# def rtt():
#     current_asn = 19165
#     flare_path = "/data/tree/%s" % current_asn
#     return render_template('rrtt.html', flare_path=flare_path)


@app.route('/collapsible_tree')
def collapsible_tree():
    current_asn = 3856
    flare_path = "/data/tree/%s" % current_asn
    return render_template('collapsible_tree.html', flare_path=flare_path)

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run()
