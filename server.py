"""PDBV server"""
from flaregen import *
from flask import Flask, render_template
from model import connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)


# Let's start to build some functions

@app.route('/data/tree/<int:asn>')
def get_tree_data(asn):
    return tree_data_json(asn)


@app.route('/data/adjacency/<int:asn>')
def get_adjacency_data(asn):
    return adjacency_data_json(asn)


@app.route('/sunburst')
def sunburst():
    current_asn = 19165
    flare_path = "/data/tree/%s" % current_asn
    return render_template('sunburst.html', flare_path=flare_path)


@app.route('/rrtt')
def rrtt():
    current_asn = 19165
    flare_path = "/data/tree/%s" % current_asn
    return render_template('rrtt.html', flare_path=flare_path)

# @app.route('/rrtt')
# def rrtt():
#     current_asn = 19165
#     flare_path = "/data/adjacency/%s" % current_asn
#     return render_template('rrtt.html')

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run()
