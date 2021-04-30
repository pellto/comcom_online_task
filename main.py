import os

from flask import Flask, render_template, request
import requests as module_request


app = Flask(__name__, static_url_path='/static')
POST_URL = f"http://{os.environ['API_PORT_5001_TCP_ADDR']}:5001/QnA"


@app.route('/')
def main_get(input_text=None):
    return render_template('QnAService.html', input_text=input_text)


@app.route('/QnAService', methods=['GET'])
def QnAService(question=None):
    if request.method == 'GET':
        question = request.args.get('question')
        params = {'text': question}
        res = module_request.post(url=POST_URL, data=params)
        print(res)
        print(res.json())
        status_code = res.status_code
        if status_code == 200:
            res = res.json()
            if len(res) < 0:
                res = "error!! :("
        else:
            return render_template('QnAService.html', question=question, result="")
        return render_template('QnAService.html', question=question, result=res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
