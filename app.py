from flask import Flask

app = Flask(__name__)
from flask import Flask, request
import mlab
from mongoengine import *
from flask_restful import Resource, Api, reqparse
mlab.connect()


app = Flask(__name__)
api = Api(app)


class User(Document):
    id_facebook = StringField()
    name = StringField()
    image_url = StringField()
    username = StringField()
    password = StringField()


userParser = reqparse.RequestParser()
userParser.add_argument("id_facebook", type=str, location="json")
userParser.add_argument("name", type=str, location="json")
userParser.add_argument("image_url", type=str, location="json")
userParser.add_argument("username", type=str, location="json")
userParser.add_argument("password", type=str, location="json")


class UserRes(Resource):

    def post(self):
        args = userParser.parse_args()
        name = args["name"]
        image_url = args["image_url"]
        username = args["username"]
        password = args["password"]

        users = User.objects((Q(username=args["username"])))
        if len(users) > 0:
            return {"status": "error", "message": "Username are have been already exist!"}, 400
        else:
            new_user = User()
            new_user.name = name
            new_user.image_url = image_url
            new_user.username = username
            new_user.password = password
            new_user.save()
            return mlab.item2json(new_user)

    def get(self):
        args = request.args
        users = User.objects((Q(username=args["username"]) & Q(password=args["password"])))
        print(len(users))
        if len(users) == 0:
            return {"status ": "error", "message": "User doesn't exist"}, 401
        else:
            print(users.first())
            return mlab.item2json(users)


class Movie(Document):
    id_user = StringField()
    id_movie = StringField()
    name = StringField()
    image_link = StringField()
    status = StringField()


movieParser = reqparse.RequestParser()
movieParser.add_argument("id_movie", type=str, location="json")
movieParser.add_argument("name", type=str, location="json")
movieParser.add_argument("image_link", type=str, location="json")
movieParser.add_argument("status", type=str, location="json")


class MovieRes(Resource):

    def get(self, id_user):
        movie_list = Movie.objects(id_user__istartswith=id_user)
        return mlab.list2json(movie_list)

    def post(self, id_user):
        args = movieParser.parse_args()
        print(id_user)
        id_user = id_user
        id_movie = args["id_movie"]
        name = args["name"]
        image_link = args["image_link"]
        status = args["status"]

        new_movie = Movie()
        new_movie.id_user = id_user
        new_movie.id_movie = id_movie
        new_movie.name = name
        new_movie.image_link = image_link
        new_movie.status = status

        new_movie.save()
        return mlab.item2json(new_movie)


api.add_resource(UserRes, "/api/user")
api.add_resource(MovieRes, "/api/movie/<id_user>")

if __name__ == '__main__':
    app.run()
