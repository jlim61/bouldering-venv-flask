from app import db
from sqlalchemy import JSON

class MoonboardBoulderModel(db.Model):
    
    __tablename__ = 'moonboard_boulders'

    id = db.Column(db.Integer, primary_key = True)
    boulder_name = db.Column(db.String, nullable = False)
    grade = db.Column(db.String, nullable = False)
    setter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    starting_hold = db.Column(JSON, nullable=False)
    usable_holds = db.Column(JSON, nullable=False)
    finish_hold = db.Column(JSON, nullable=False)
    moonboard_configuration = db.Column(db.String)

    def __repr__(self):
        return f'<Moonboard Boulder:\n{self.boulder_name}\n{self.grade}\n{self.setter_id}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()