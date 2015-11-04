
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey

engine = create_engine("mysql://root@localhost/peeringdb")
session = Session(engine)

metadata = MetaData()
metadata.reflect(engine)


Base = automap_base()
Base.prepare(engine, reflect=True)
# defining the actual tables.  I know it works because they have columns!
MgmtFacilities = Base.classes.mgmtFacilities
MgmtPublics = Base.classes.mgmtPublics
MgmtPublicsFacilities = Base.classes.mgmtPublicsFacilities
MgmtPublicsIPs = Base.classes.mgmtPublicsIPs
PeerParticipantsPublics = Base.classes.peerParticipantsPublics
PeerParticipantsContacts = Base.classes.peerParticipantsContacts
PeerParticipantsPrivates = Base.classes.peerParticipantsPrivates
PeerParticipants = Base.classes.peerParticipants

db = SQLAlchemy() #wait, I don't use this?!?!
# for the above, have to explicitly declare some classes:

class PeerParticipantsPublics(Base):
    __tablename__ = "peerParticipantsPublics"
# necessary to extend tables we'd created above!
    __table_args__ = {'extend_existing': True} 
# override two of the columns to have foreign keys in them
    participant_id = db.Column(db.Integer, db.ForeignKey('peerParticipants.id'))
    public_id = db.Column(db.Integer, db.ForeignKey('mgmtPublics.id'))

# further let's define some relationships so that we may "walk"
    mgmtPublics = db.relationship ("MgmtPublics", backref = db.backref("id"))
    peerParticipants = db.relationship("PeerParticipants", backref = db.backref("id"))

# finally, let's make a quaint repr: (to-do)    
#Have to seed the tables as well, right?


# db.session.execute(query, dictionary-of-values)
public_id = 1
QUERY = "select * from peerParticipantsPublics where public_id=:public_id"
cursor = session.execute(QUERY, {'public_id': public_id}) #removed the db from db.session.
results = cursor.first()
print results

#What about a move fancy query?  And remember, don't have to do joins, since we now have backrefs!
#for example, start at mgmtPublics table, and get to peerParticipantsPublics

