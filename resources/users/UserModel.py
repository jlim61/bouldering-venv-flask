from app import db

from werkzeug.security import generate_password_hash, check_password_hash

# from ..moonboard_boulders.MoonboardBoulderModel import MoonboardBoulderModel

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))    
)

projected_boulders = db.Table('projected_boulders',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('moonboard_boulder_id', db.Integer, db.ForeignKey('moonboard_boulders.id')),
    db.Column('completed', db.Boolean, default=False),
    db.Column('attempts', db.Integer, default=0)
)

class UserBoulderProjects(db.Model):

    __tablename__ = 'boulder_projects'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    boulder_id = db.Column(db.Integer, db.ForeignKey('moonboard_boulders.id'))
    completed = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    moonboard_boulders = db.relationship('MoonboardBoulderModel', back_populates='projected_by')

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password_hash = db.Column(db.String, nullable = False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    setter = db.Column(db.Boolean)
    gym_boulders = db.relationship('GymBoulderModel', backref='creator', lazy='dynamic', cascade='all, delete')
    moonboard_boulders = db.relationship('MoonboardBoulderModel', backref='creator', lazy='dynamic', cascade='all, delete')
    followed = db.relationship('UserModel',
        secondary=followers,
        primaryjoin = followers.c.follower_id == id,
        secondaryjoin = followers.c.followed_id == id,
        backref = db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
    projected = db.relationship('UserBoulderProjects',
        backref='projects'
    )

    def __repr__(self):
        return f'<User: {self.username}'
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def from_dict(self, dict):
        password = dict.pop('password')
        self.hash_password(password)
        for k, v in dict.items():
            setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def is_following(self, user):
        return self.followed.filter(user.id == followers.c.followed_id).count() > 0
    
    def follow_user(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            self.save()

    def unfollow_user(self,user):
        if self.is_following(user):
            self.followed.remove(user)
            self.save()

    # def get_projects(self):
    #     print(UserBoulderProjects.query.filter(UserBoulderProjects.c.user_id == self.id).all())

    def is_projecting(self, boulder):
        return UserBoulderProjects.query.filter(boulder.id == UserBoulderProjects.boulder_id , self.id == UserBoulderProjects.user_id).count() > 0
    
    def add_project(self, boulder):
        if not self.is_projecting(boulder):
            new_boulder = UserBoulderProjects(user_id = self.id, boulder_id = boulder.id)
            db.session.add(new_boulder)
            db.session.commit()

    def remove_project(self,boulder):
        if self.is_projecting(boulder):
            boulder_to_remove = UserBoulderProjects(user_id = self.id, boulder_id = boulder.id)
            db.session.delete(boulder_to_remove)
            db.session.commit()