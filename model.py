from flask import Flask
from flask_sqlalchemy import SQLAlchemy


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

class MgmtPublics(db.Model):
    __tablename__ = 'mgmtPublics'
    __table_args__ = {'extend_existing': True}


    def __repr__(self):
        return '<MgmtPublics id=%r name=%r city=%r country=%r>' %(
            self.id, self.name, self.city, self.country)


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

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
