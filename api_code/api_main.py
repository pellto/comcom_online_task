import json

import torch
from flask import Flask, make_response
from flask_restx import Api, Resource, reqparse
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast


app = Flask(__name__)
api = Api(app)


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("MODEL LOADING ...")
MODEL = GPT2LMHeadModel.from_pretrained("./models")
MODEL.to(DEVICE)
print("TOKENIZER LOADING ...")
TOKENIZER = PreTrainedTokenizerFast.from_pretrained("taeminlee/kogpt2")
MODEL.eval()


def generate(text=""):
    if text == "":
        return "error!! :("

    input_ids = text + "</s>"
    tokens = TOKENIZER.encode(input_ids, return_tensors='pt').to(DEVICE)
    min_length = len(tokens)
    output_ids = TOKENIZER.decode(MODEL.generate(
        tokens,
        do_sample=True,
        max_length=50,
        min_length=min_length,
        top_k=50,
        top_p=0.92,
        num_return_sequences=1
    )[0], skip_special_tokens=True)
    return output_ids[len(text):]


@api.route("/QnA")
@api.doc(params={
   'text': {
      'description':"INPUT YOUR QUESTION"
   }
})
class QnAServiceAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        text = parser.parse_args()['text']
        output_ids = generate(text)
        return make_response(json.dumps(output_ids, ensure_ascii=False))


api.add_resource(QnAServiceAPI, '/QnA')


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5001)
