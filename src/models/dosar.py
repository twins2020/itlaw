from src.db import db
import uuid


class DosarModel(db.Model):
    __tablename__ = 'dosare'

    dosarType = {'fond': 'Fond', 'apel': 'Apel', 'recurs': 'Recurs', 'contestatie': 'Contestatie In Anulare',
                 'revizuire': 'Revizuire', 'executare': 'Executare Silita',
                 'faliment': 'Cerere Inscriere la Masa Credala (faliment)'}

    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(60))
    type = db.Column(db.String(50))

    __table_args__ = (db.UniqueConstraint('name', 'type', name='name_type_uq'),)

    def __init__(self, name, _type, _id=None):
        self.id = _id if _id else str(uuid.uuid4().hex)
        self.name = name
        self.type = _type if DosarModel.validate_type(_type) else None

    @staticmethod
    def validate_type(type):
        return DosarModel.dosarType.get(type)

    def json(self):
        return {'name': self.name, 'type': DosarModel.dosarType.get(self.type)}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
