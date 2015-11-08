"""PDBV server"""

from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db

app = Flask(__name__)

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run()


# Let's start to build some functions
@app.route('/mgmtPublics')
def get_all_mgmtPublics():
    """"""
    pass

    all_publics = MgmtPublics.query.all()
    MgmtPublics.get_all_json()
    [public.to_dict() for public in all_publics]

    return jsonified()
