"""PDBV server"""

from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db

app = Flask(__name__)

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run()
