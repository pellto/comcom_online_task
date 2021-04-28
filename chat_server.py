import os
from flask import Flask, render_template, request
import requests as module_request


app = Flask(__name__, static_url_path='/static')
POST_URL = f"http://{os.environ['API_PORT_5001_TCP_ADDR']}:5001"

previous_bot = []
USER = []
BOT = []


def response_parser(response, user_index=0):
    start = response.index("<s>") + 4
    end = response[start:].index("</s>") + start
    return response[start:end]

def chatbot_parser(response, user_index=0):
    start = response.index("</s>") + 5
    end = response[start:].index("<s>") + start
    return response[start:end]

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
        params = {'input_text': question}
        res = module_request.post(url=POST_URL + "/QnA", json=params)
        status_code = res.status_code
        if status_code == 200:
            res = response_parser(res.json())
        else:
            return render_template('QnAService.html', question=question, result="")
        return render_template('QnAService.html', question=question, result=res)


@app.route('/QnAChatbot', methods=['GET'])
def QnAChatbot(user_input=None):
    if request.method == 'GET':
        user_input = request.args.get('user_input')
        _input = f"{previous_bot[0]} {user_input}" if len(previous_bot) >= 1 else f"{user_input}"
        print(_input)
        USER.append(user_input)
        params = {'input_text': _input, 'early_stop': False}
        res = module_request.post(url=POST_URL+"/Chatbot", json=params)
        print(res.json())
        status_code = res.status_code
        if status_code == 200:
            try:
                res = chatbot_parser(res.json())
            except:
                res = response_parser(res.json())
            BOT.append(res)
        else:
            return render_template('QnAChatbot.html', history_length=0, user=[], bot=[], current_input='')

        if len(previous_bot) > 0:
            previous_bot.pop()
        previous_bot.append(res)

        return render_template('QnAChatbot.html', history_length=len(USER), user=USER, bot=BOT, current_input=user_input)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
