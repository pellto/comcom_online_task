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
@api.doc(params={
   'input_text': {
      'description':"INPUT YOUR TEXT"
   },
   "num_beam": {
      'description':"""Search Method in generate sentence\nif you want top-method, num_beam=-1"""
   },
   "early_stop": {
      'description':"early-stop method",
      'type': 'bool'
   }
})
class OriginalLongPost(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('input_text', type=str, help="input_text")
      parser.add_argument('num_beams', type=int, help="numbeams")
      parser.add_argument('early_stop', type=bool, help="es")
      args = parser.parse_args()
      ret = {'max_length':150}
      for arg in args:
         ret[arg] = args[arg]
      data = API_models.generate_sentence_getter(ret)
      return data


@api.route("/Original/short")
@api.doc(params={
   'input_text': {
      'description':"INPUT YOUR TEXT"
   },
   "num_beam": {
      'description':"""Search Method in generate sentence\nif you want top-method, num_beam=-1"""
   },
   "early_stop": {
      'description':"early-stop method",
      'type': 'bool'
   }
})
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
   @api.doc(params={
      'input_text': {
         'description': "INPUT YOUR TEXT"
      },
      "early_stop": {
         'description': "early-stop method",
         'type': 'bool'
      }
   })
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
@api.doc(params={
   'input_text': {
      'description':"INPUT YOUR TEXT"
   },
   "early_stop": {
      'description':"early-stop method",
      'type': 'bool'
   }
})
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
@api.doc(params={
   'input_text': {
      'description':"INPUT YOUR TEXT"
   },
   "early_stop": {
      'description':"early-stop method",
      'type': 'bool'
   }
})
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
@api.doc(params={
   'input_text': {
      'description':"INPUT YOUR TEXT"
   },
   "early_stop": {
      'description':"early-stop method",
      'type': 'bool'
   }
})
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