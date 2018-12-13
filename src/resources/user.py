from flask_restful import Resource, reqparse
from src.models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('name',
                        type=str,
                        required=False,
                        )
    parser.add_argument('user_type',
                        type=str,
                        required=False,
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "Un utilizator cu acest nume deja exista"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "Utilizatorul a fost creat."}, 201
