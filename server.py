"""PDBV server"""

from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, PeerParticipants, MgmtPublics, PeerParticipantsPublics

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
