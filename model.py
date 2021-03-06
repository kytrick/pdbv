import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# import json
# import networkx as nx
# from networkx.readwrite import json_graph
# from flaregen import flare_tree_as_json_for_asn, tree_data_json
# from flaregen import adjacency_data_json, sunburst_ready_json
# from flaregen import asn_search, tree_ready_json


def connect_to_db(app):
    if 'RDS_HOSTNAME' in os.environ:
        DB = {
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            }
    else:
        DB = {
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            }

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/peeringdb' % (
        DB['USER'],
        DB['PASSWORD'],
        DB['HOST'],
        )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.reflect()
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 300
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 10

# enable autocommit to dsiable implicit transactions
# http://docs.sqlalchemy.org/en/rel_0_8/orm/session.html#autocommit-mode
db = SQLAlchemy(session_options={
    'autocommit': True,
    'autoflush': False,
    'expire_on_commit': False
    })
app = Flask('pdbv_model')
connect_to_db(app)


class BaseTable(object):
    __table_args__ = {'extend_existing': True}

    def serialize(self, cols_to_use=None):
        """Returns object data that is serializable"""
        result = {}
        for key in self.__table__.columns.keys():
            value = getattr(self, key)
            if not cols_to_use or key in cols_to_use:
                if isinstance(value, datetime.datetime):
                    result[key] = str(value)
                else:
                    result[key] = value
        return result


class PeerParticipants(db.Model, BaseTable):
    __tablename__ = 'peerParticipants'

    def __repr__(self):
        return '<PeerParticipants id=%r asn=%r name=%r info_traffic=%r>' % (
            self.id, self.asn, self.name, self.info_traffic)


class MgmtPublics(db.Model, BaseTable):
    __tablename__ = 'mgmtPublics'

    def __repr__(self):
        return '<MgmtPublics id=%r region=%r country=%r city=%r name=%r>' % (
            self.id, self.region_continent, self.country, self.city, self.name)


class PeerParticipantsPublics(db.Model, BaseTable):
    __tablename__ = 'peerParticipantsPublics'

    # override two of the columns to have foreign keys in them
    participant_id = db.Column(
        db.Integer, db.ForeignKey('peerParticipants.id'))
    public_id = db.Column(db.Integer, db.ForeignKey('mgmtPublics.id'))

    # further let's define some relationships so that we may "walk"
    peerParticipants = db.relationship(
        'PeerParticipants', backref=db.backref('peerParticipantsPublics'))
    mgmtPublics = db.relationship(
        'MgmtPublics', backref=db.backref('peerParticipantsPublics'))

    def __repr__(self):
        return '<PeerParticipantsPublics id=%s local_asn=%s speed=%s>' % (
            self.id, self.local_asn, self.speed)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
