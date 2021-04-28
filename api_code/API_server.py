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
   }
})
class OriginalLongPost(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('input_text', type=str)
      args = parser.parse_args()
      ret = {'max_length':200, "input_text":args['input_text']}
      data = API_models.generate_sentence_getter(ret)
      return data


@api.route("/Original/short")
@api.doc(params={
   'input_text': {
      'description':"INPUT YOUR TEXT"
   }
})
class OriginalShortPost(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('input_text', type=str)
      args = parser.parse_args()
      ret = {'max_length':100, "input_text":args['input_text']}
      data = API_models.generate_sentence_getter(ret)
      return data


@api.route("/QnA")
@api.doc(params={
   'input_text': {
      'description':"INPUT YOUR TEXT"
   }
})
class QnAShort(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('input_text', type=str)
      args = parser.parse_args()
      ret = {'max_length':200, "input_text":args['input_text']}
      data = API_models.generate_answer_getter(ret)
      return data


@api.route("/Chatbot")
@api.doc(params={
   'input_text': {
      'description':"INPUT YOUR TEXT"
   }
})
class ServiceShort(Resource):
   def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument('input_text', type=str)
      args = parser.parse_args()
      ret = {'max_length':200, "input_text":args['input_text']}
      data = API_models.generate_answer_getter(ret)
      return data



api.add_resource(OriginalLongPost, '/Original/long')
api.add_resource(OriginalShortPost, '/Original/short')
api.add_resource(QnAShort, '/QnA')
api.add_resource(ServiceShort, '/Chatbot')



if __name__ == '__main__':
   app.run(host='0.0.0.0', port='5001', debug=True)