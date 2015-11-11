from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json



def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/peeringdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.reflect()

db = SQLAlchemy()
app = Flask('pdbv_model')
connect_to_db(app)


class PeerParticipants(db.Model):
    __tablename__ = 'peerParticipants'
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return '<PeerParticipants id=%r asn=%r name=%r info_traffic=%r>' %(
            self.id, self.asn, self.name, self.info_traffic)

    def serialize(self):
        """Returns object data that is serializable"""
        return{

            'id': self.id,
             'asn': self.asn,
             'name': self.name,
             'aka': self.aka,
             'website': self.website,
             'notes_public': self.notes_public,
             'notes_private': self.notes_private,
             'irr_as_set': self.irr_as_set,
             'info_traffic': self.info_traffic,
             'info_ratio': self.info_ratio,
             'info_scope': self.info_scope,
             'info_type': self.info_type,
             'info_prefixes': self.info_prefixes,
             'info_lookingglass': self.info_lookingglass,
             'info_routeserver': self.info_routeserver,
             'info_unicast': self.info_unicast,
             'info_multicast': self.info_multicast,
             'info_ipv6': self.info_ipv6,
             'policy_url': self.policy_url,
             'policy_general': self.policy_general,
             'policy_locations': self.policy_locations,
             'policy_ratio': self.policy_ratio,
             'policy_contracts': self.policy_contracts,
             'policy_nopublic': self.policy_nopublic,
             'policy_noprivate': self.policy_noprivate,
             'date_created': self.date_created,
             'date_lastupdated': self.date_lastupdated
        }



class MgmtPublics(db.Model):
    __tablename__ = 'mgmtPublics'
    __table_args__ = {'extend_existing': True}


    def __repr__(self):
        return '<MgmtPublics id=%r name=%r city=%r country=%r>' %(
            self.id, self.name, self.city, self.country)

    def serialize(self):
        """Returns object data that is serializeable"""
        return {

             'id': self.id,
             'approved': self.approved,
             'name': self.name,
             'name_long': self.name_long,
             'ipaddr': self.ipaddr,
             'city': self.city,
             'country': self.country,
             'region_continent': self.region_continent,
             'media': self.media,
             'tech_email': self.tech_email,
             'tech_phone': self.tech_phone,
             'policy_email': self.policy_email,
             'policy_phone': self.policy_phone,
             'website': self.website,
             'url_stats': self.url_stats,
             'proto_unicast': self.proto_unicast,
             'proto_multicast': self.proto_multicast,
             'proto_ipv6': self.proto_ipv6
        }

class PeerParticipantsPublics(db.Model):
    __tablename__ = 'peerParticipantsPublics'
    __table_args__ = {'extend_existing': True}

    # override two of the columns to have foreign keys in them
    participant_id = db.Column(db.Integer, db.ForeignKey('peerParticipants.id'))
    public_id = db.Column(db.Integer, db.ForeignKey('mgmtPublics.id'))

    # further let's define some relationships so that we may "walk"
    peerParticipants = db.relationship('PeerParticipants', backref=db.backref('peerParticipantsPublics'))
    mgmtPublics = db.relationship('MgmtPublics', backref=db.backref('peerParticipantsPublics'))


    def __repr__(self):
        return '<PeerParticipantsPublics id=%s local_asn=%s speed=%s>' % (
            self.id, self.local_asn, self.speed)

    def serialize(self):
        """Returns object data that is serializeable"""
        return {

             'id': self.id,
             'participant_id': self.participant_id,
             'public_id': self.public_id,
             'local_asn': self.local_asn,
             'local_ipaddr': self.local_ipaddr,
             'speed': self.speed,
             'protocol': self.protocol,
             'pending': self.pending
        }






if __name__ == "__main__":
    from server import app
    connect_to_db(app)
