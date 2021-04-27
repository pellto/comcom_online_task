import json
from flask import Flask
from flask_restx import Api, Resource, reqparse

import API_models


app = Flask(__name__)
api = Api(app)


@api.route('/hello')
class HelloWorld(Resource):
   def get(self):
      return json.dumps({'hello':'world!'})


@api.route("/Original/long")
class OriginalLongPost(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('input_text', type=str)
      parser.add_argument('num_beams', type=int)
      parser.add_argument('early_stop', type=bool)
      args = parser.parse_args()
      ret = {'max_length':150}
      for arg in args:
         ret[arg] = args[arg]
      data = API_models.generate_sentence_getter(ret)
      return data


@api.route("/Original/short")
class OriginalShortPost(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('input_text', type=str)
      parser.add_argument('num_beams', type=int)
      parser.add_argument('early_stop', type=bool)
      args = parser.parse_args()
      ret = {'max_length':40}
      for arg in args:
         ret[arg] = args[arg]
      data = API_models.generate_sentence_getter(ret)
      return data


@api.route("/QnA/long")
class QnALong(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('input_text', type=str)
      parser.add_argument('early_stop', type=bool)
      args = parser.parse_args()
      ret = {'max_length':150}
      for arg in args:
         ret[arg] = args[arg]
      data = API_models.generate_answer_getter(ret)
      return data


@api.route("/QnA/short")
class QnAShort(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('input_text', type=str)
      parser.add_argument('early_stop', type=bool)
      args = parser.parse_args()
      ret = {'max_length':40}
      for arg in args:
         ret[arg] = args[arg]
      data = API_models.generate_answer_getter(ret)
      return data


@api.route("/Service/long")
class ServiceLong(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('input_text', type=str)
      parser.add_argument('early_stop', type=bool)
      args = parser.parse_args()
      ret = {'max_length':150}
      for arg in args:
         ret[arg] = args[arg]
      data = API_models.generate_answer_getter(ret)
      return data


@api.route("/Service/short")
class ServiceShort(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('input_text', type=str)
      parser.add_argument('early_stop', type=bool)
      args = parser.parse_args()
      ret = {'max_length':40}
      for arg in args:
         ret[arg] = args[arg]
      data = API_models.generate_answer_getter(ret)
      return data



api.add_resource(OriginalLongPost, '/Original/long')
api.add_resource(OriginalShortPost, '/Original/short')
api.add_resource(QnALong, '/QnA/long')
api.add_resource(QnAShort, '/QnA/short')
api.add_resource(ServiceShort, '/Service/short')
api.add_resource(ServiceLong, '/Service/long')



if __name__ == '__main__':
   app.run(host='0.0.0.0', port='25000', debug=True)