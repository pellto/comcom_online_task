from flask import Flask, render_template, request
import requests as module_request


app = Flask(__name__, static_url_path='/static')
POST_URL = "http://203.246.112.132:25000"

previous_bot = []
USER = []
BOT = []


def response_parser(response, user_index=0):
    start = user_index + response[user_index:].index("<s> ") + 4
    end = start + min(response[start:].index('<s>'), response[start:].index('</s>'))
    return response[start:end]


@app.route('/')
def main_get(input_text=None):
    return render_template('index.html', input_text=input_text)


@app.route('/KoGPT2_demo', methods=['GET'])
def KoGPT2_demo(input_text=None):
    if request.method == 'GET':
        input_text = request.args.get('input_text')
        _type = request.args.get('_type')
        length = request.args.get('length')
        params = {'input_text': input_text, "do_sample":_type}
        res = module_request.post(url=POST_URL + f"/Original/{length}", json=params)
        status_code = res.status_code
        if status_code == 200:
            res = res.json()
        else:
            return render_template('KoGPT_api_demo.html', input_text=input_text, _type=str(_type), result=res)
    return render_template('KoGPT_api_demo.html', input_text=input_text, _type=str(_type), result=res)


@app.route('/QnAService', methods=['GET'])
def QnAService(question=None):
    if request.method == 'GET':
        question = request.args.get('question')
        _type = request.args.get('_type')
        params = {'input_text': question, "do_sample": _type}
        res = module_request.post(url=POST_URL + f"/QnA/{_type}", json=params)
        status_code = res.status_code
        if status_code == 200:
            res = response_parser(res.json())
        else:
            return render_template('KoGPT_api_demo.html', input_text=question, _type=str(_type), result="")
        return render_template('QnAService.html', question=question, _type=_type, result=res)


@app.route('/QnAChatbot', methods=['GET'])
def QnAChatbot(user_input=None):
    if request.method == 'GET':
        bot_answer = request.args.get('bot_answer')
        user_input = request.args.get('user_input')
        _input = f"{previous_bot[0]}<s>{user_input}" if len(USER) > 1 else f"{user_input}"
        USER.append(user_input)
        if len(previous_bot) > 0:
            params = {'input_text': _input, 'early_stop': False}
        else:
            params = {'input_text': _input, 'early_stop': False}
        res = module_request.post(url=POST_URL+f"/Service/{bot_answer}", json=params)
        status_code = res.status_code

        if status_code == 200:
            res = response_parser(res.json(), len(_input)) if len(BOT) > 0 else response_parser(res.json())
            BOT.append(res)
        else:
            return render_template('QnAChatbot.html', history_length=0, user=[], bot=[], current_input='')

        if len(previous_bot) > 0:
            previous_bot.pop()
        previous_bot.append(res)

        return render_template('QnAChatbot.html', history_length=len(USER), user=USER, bot=BOT, current_input=user_input)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
