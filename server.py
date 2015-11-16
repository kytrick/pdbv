"""PDBV server"""
from flaregen import *
from flask import Flask
from model import connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run()


# Let's start to build some functions
@app.route('/mgmtPublics')
# TODO: Use query parameters to get asn. /mgmtPublics/1
def get_all_mgmtPublics():
    """"""

    # get all locations for an AS
    results = PeerParticipantsPublics.flare_tree_as_json_for_as(asn)
    # TODO: eturn json to browser
    return results


@app.route('/data/<asn>')
def get_tree_data(asn):
    return tree_data_json(asn)


@app.route('/sunburst')
def sunburst():
    return Flask.render_template('sunburst.html')


@app.route('/rrtt')
def rrtt():
    return Flask.render_template('rrtt.html')
