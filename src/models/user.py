from src.db import db
from sqlalchemy_utils import UUIDType, ChoiceType
import uuid


class UserModel(db.Model):
    __tablename__ = 'users'

    TYPES = [
        ('regular', 'Avocat'),
        ('admin', 'Administrator')
    ]

    id = db.Column(db.String(120), primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    name = db.Column(db.String(160))
    user_type = db.Column(ChoiceType(TYPES))

    def __init__(self, username, password, _id=None, name=None, user_type="regular"):
        self.id = _id if _id else str(uuid.uuid4().hex)
        self.username = username
        self.password = password
        self.name = name if name else username
        self.user_type = user_type

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'id:''username': self.username, 'name': self.name, 'user_type': self.user_type.value }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
