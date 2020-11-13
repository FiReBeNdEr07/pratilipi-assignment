from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import os

DB_USERNAME=os.environ['MY_MYSQL_USER']
DB_PASSWORD=os.environ['MY_MYSQL_PASSWORD']
DB_HOST=os.environ['MY_MYSQL_HOST']
DATABASE_NAME=os.environ['MY_DATABASE_NAME']
DB_URI = 'mysql+pymysql://%s:%s@%s:3306/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=DB_URI
db = SQLAlchemy(app)

###Models####
class Anime(db.Model):
    __tablename__ = "animes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))


    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,title):
        self.title = title
    def __repr__(self):
        return '' % self.id
db.create_all()
class AnimeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Anime
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    title = fields.String(required=True)

@app.route('/',methods=['GET'])
def get():
    return jsonify({'msg':'Hello Mani!'})

@app.route('/animes', methods = ['GET'])
def index():
    get_animes = Anime.query.all()
    anime_schema = AnimeSchema(many=True)
    animes = anime_schema.dump(get_animes)
    return make_response(jsonify({"anime": animes}))
@app.route('/animes/<id>', methods = ['GET'])
def get_anime_by_id(id):
    get_anime = Anime.query.get(id)
    anime_schema = AnimeSchema()
    anime = anime_schema.dump(get_anime)
    return make_response(jsonify({"anime": anime}))
@app.route('/animes/<id>', methods = ['DELETE'])
def delete_anime_by_id(id):
    get_anime = Anime.query.get(id)
    db.session.delete(get_anime)
    db.session.commit()
    return make_response("",204)
@app.route('/animes', methods = ['POST'])
def create_anime():
    data = request.get_json()
    anime_schema = AnimeSchema()
    anime = anime_schema.load(data)
    result = anime_schema.dump(anime.create())
    return make_response(jsonify({"anime": result}),200)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000,debug=True)