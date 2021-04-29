import os
from flask import Flask, render_template, request
import requests as module_request


app = Flask(__name__, static_url_path='/static')
POST_URL = f"http://{os.environ['API_PORT_5001_TCP_ADDR']}:5001"

MULTI_TURN = []
USER = []
BOT = []


@app.route('/')
def main_get(input_text=None):
    return render_template('index.html', input_text=input_text)


@app.route('/KoGPT2_demo', methods=['GET'])
def KoGPT2_demo(input_text=None):
    if request.method == 'GET':
        input_text = request.args.get('input_text')
        length = request.args.get('length')
        params = {'input_text': input_text}
        res = module_request.post(url=POST_URL + f"/Original/{length}", json=params)
        status_code = res.status_code
        if status_code == 200:
            res = res.json()
        else:
            return render_template('KoGPT_api_demo.html', input_text=input_text, result=res)
    return render_template('KoGPT_api_demo.html', input_text=input_text, result=res)


@app.route('/QnAService', methods=['GET'])
def QnAService(question=None):
    if request.method == 'GET':
        question = request.args.get('question')
        print(question)
        params = {'input_text': question}
        res = module_request.post(url=POST_URL + "/QnA", json=params)
        print(res.json())
        status_code = res.status_code
        if status_code == 200:
            res = res.json()[len(question):]
        else:
            return render_template('QnAService.html', question=question, result="")
        return render_template('QnAService.html', question=question, result=res)


@app.route('/QnAChatbot', methods=['GET'])
def QnAChatbot(user_input=None):
    if request.method == 'GET':
        user_input = request.args.get('user_input')
        _input = ""
        if len(MULTI_TURN) >= 1:
            _input = " ".join(MULTI_TURN)
        _input = _input + f" {user_input}</s>"
        input_length = len(_input) - 4
        print(_input)

        MULTI_TURN.append(_input[:-4])
        USER.append(user_input)
        params = {'input_text': _input, 'early_stop': False}
        res = module_request.post(url=POST_URL+"/Chatbot", json=params)
        print(res.json())
        status_code = res.status_code
        if status_code == 200:
            res = res.json()[input_length:]
            BOT.append(res)
        else:
            return render_template('QnAChatbot.html', history_length=0, user=[], bot=[], current_input='')

        MULTI_TURN.append(res)
        if len(MULTI_TURN) >= 5:
            MULTI_TURN.pop()

        return render_template('QnAChatbot.html', history_length=len(USER), user=USER, bot=BOT, current_input=user_input)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
