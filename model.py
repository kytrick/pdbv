from collections import defaultdict, Counter
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import networkx as nx
from networkx.readwrite import json_graph



def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/peeringdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.reflect()

db = SQLAlchemy()
app = Flask('pdbv_model')
connect_to_db(app)


def flare_tree_as_json_for_asn(asn):
    """ Returned a json representation of an AS tree """
    # continent_count = Counter()
    # country_count = Counter()
    # city_count = Counter()
    # exchanges = defaultdict(lambda: defaultdict(lambda: defaultdict()))
    # results = MgmtPublics.query.filter(PeerParticipants.asn == asn).all()
    results = MgmtPublics.query.join(
        PeerParticipantsPublics).filter(
        PeerParticipantsPublics.local_asn == asn).all()

    H = nx.DiGraph()   # initialize the tree
    H.add_node("asn")  # this is the root

    for result in results:  # each result here is an IX
        H.add_nodes_from([
            result.region_continent, result.country, result.city, result.name])

        H.add_edge("asn", result.region_continent)
        H.add_edge(result.region_continent, result.country)
        H.add_edge(result.country, result.city)
        H.add_edge(result.city, result.name)

    # return json.dumps(json_graph.tree_data(H, root=asn))
    return H

def sunburst_ready_json(asn):
    H = flare_tree_as_json_for_asn(asn)
    return json.dumps(json_graph.tree_data(H, root=asn))

def tree_ready_json(asn):
    H = flare_tree_as_json_for_asn(asn)
    return json.dumps(json_graph.adjacency_data(H))

def otherthing():
    pass




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
