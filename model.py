from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/peeringdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.reflect()

db = SQLAlchemy()
app = Flask(__name__)
connect_to_db(app)


class PeerParticipants(db.Model):
    __tablename__ = 'peerParticipants'
    __table_args__ = {'extend_existing': True}


class MgmtPublics(db.Model):
    __tablename__ = 'mgmtPublics'
    __table_args__ = {'extend_existing': True}


class PeerParticipantsPublics(db.Model):
    __tablename__ = 'peerParticipantsPublics'
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return '<PeerParticipantsPublics id=%s local_asn=%s speed=%s>' % (
            self.id, self.local_asn, self.speed)

    # override two of the columns to have foreign keys in them
    participant_id = db.Column(db.Integer, db.ForeignKey('peerParticipants.id'))
    public_id = db.Column(db.Integer, db.ForeignKey('mgmtPublics.id'))

    # further let's define some relationships so that we may "walk"
    peerParticipants = db.relationship('PeerParticipants', backref=db.backref('participant_id'))
    mgmtPublics = db.relationship('MgmtPublics', backref=db.backref('public_id'))





# PeerParticipants = Table('PeerParticipants', db.metadata, autoload=True, autoload_with=db.engine)
