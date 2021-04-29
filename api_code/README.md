# comcom_online_task (API)
커먼컴퓨터 지원 온라인 과제


# Pellto's KoDialog API

## 사용법
1. [해당 레포지토리](https://github.com/pellto/comcom_online_task)를 다운로드 한 후 압축을 풀어 주세요.

2. move directory
```bash
mv api_code
```

3. docker Build
```bash
docker build -server -t api-server .
```

4. run docker container
```bash
docker run -d -p 5001:5001 --name api-server api-server
```

## with browser
1. [open browser](http://127.0.0.1:5001)

- /Original/long
  - Use Original KoGPT-2 generater
  - parameter :
    - input_text : input_text for generate long Sentence
<br>
- /Original/short
  - Use Original KoGPT-2 generater
  - parameter :
    - input_text : input_text for generate short Sentence
<br>
- /QnA
  - Use Fine-Tuned KoGPT-2 generater with [simple QnA Dataset](https://github.com/songys/Chatbot_data)
  - parameter :
    - input_text : Simple Question
<br>
- /Chatbot
  - Use Fine-Tuned KoGPT-2 generater with [Korean Dialog Data](https://aihub.or.kr/aidata/85)
  - parameter :
    - input_text : Store-related Sentence or Question
