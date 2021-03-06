"""PDBV server"""

from flaregen import (
    adjacency_data_json,
    flare_tree_as_json_for_asn,
    live_search,
    sunburst_ready_json,
    tree_data_json,
    tree_ready_json,
    )

from flask import Flask, render_template, request, url_for, redirect
from flask.ext.bower import Bower
#from flask_sslify import SSLify

from model import connect_to_db

app = Flask(__name__)
Bower(app)  # This provides the /bower url route
#sslify = SSLify(app, age=300) # This attaches SSLify to the app
#sslify = SSLify(app, permanent=True) 


@app.route('/')
def index():
    return render_template("base.html")


@app.route('/about')
def about():
    return render_template("about.html")


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


@app.route('/livesearch/<query>')
def typesearch(query):
    return '%s' % live_search(query)

if __name__ == "__main__":
    app.config['SQLALCHEMY_ECHO'] = True
    app.debug = True
    connect_to_db(app)
    app.run()
else:
    import logging
    logger = logging.getLogger(__name__)
    FORMAT = "[%(asctime)s %(levelname)s %(name)s:%(module)s %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
