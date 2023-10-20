from app import db

class GymBoulderModel(db.Model):
    
    __tablename__ = 'gym_boulders'

    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String, nullable = False)
    grade = db.Column(db.String, nullable = False)
    setter_id = db.Column(db.Integer, db.ForeignKey('setters.id'))

    def __repr__(self):
        return f'<Gym Boulder:\n{self.grade}\n{self.setter_id}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()