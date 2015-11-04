"""PDBV server"""

from flask import Flask, render_template, request, flash, redirect, session
#from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Asn


app = Flask(__name__)

@app.route('/sunburst')
def sunburst():
    """sunburst"""

    return render_template("templates/sunburst.html")

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run()
