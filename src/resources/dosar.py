from flask_restful import Resource, reqparse
from src.models.dosar import DosarModel
from flask_jwt import jwt_required


class Dosar(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        required=True,
                        help="Dosarul trebuie sa aiba un numar!"
                        )
    parser.add_argument('_type',
                        required=False,
                        help="Dosarul trebuie sa aiba un tip!"
                        )
    @jwt_required()
    def get(self):
        data = Dosar.parser.parse_args()
        dosar = DosarModel.find_by_name(data['name'])
        if dosar:
            return dosar.json()
        return {'message': 'Dosar inexistent'}, 404

    @jwt_required()
    def post(self):
        data = Dosar.parser.parse_args()
        dosar = DosarModel.find_by_name(data['name'])
        if dosar and dosar.type == data['_type'] :
            return {'message': 'Exista deja un dosar cu numarul "{}" si tipul "{}"'.format(data['name'], data['_type'])}, 400

        dosar = DosarModel(**data)

        try:
            dosar.save_to_db()
        except:
            return {"message": "A aparut o eroare. Va rugam incercati din nou"}, 500

        return dosar.json(), 201

    @jwt_required()
    def delete(self):
        data = Dosar.parser.parse_args()
        dosar = DosarModel.find_by_name(data['name'])
        if dosar:
            dosar.delete_from_db()

        return {'message': 'Dosarul a fost sters.'}

    @jwt_required()
    def put(self):
        data = Dosar.parser.parse_args()

        dosar = DosarModel.find_by_name(data['name'])

        if dosar:
            dosar.type = data['_type']
        else:
            dosar = DosarModel(**data)

        dosar.save_to_db()

        return dosar.json()


class DosarList(Resource):
    @jwt_required()
    def get(self):
        return {'dosare': list(map(lambda x: x.json(), DosarModel.query.all()))}
