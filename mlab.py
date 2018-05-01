#mongodb://<dbuser>:<dbpassword>@ds027425.mlab.com:27425/techfood
import mongoengine
import json

#mongodb://<dbuser>:<dbpassword>@ds161048.mlab.com:61048/kingcua

#mongodb://<dbuser>:<dbpassword>@ds163689.mlab.com:63689/movie_shelf

host = "ds163689.mlab.com"
port = 63689
db_name = "movie_shelf"
user_name = "cuong"
password = "cuong"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)


def list2json(l):
   return [json.loads(item.to_json()) for item in l]


def item2json(item):
   return json.loads(item.to_json())