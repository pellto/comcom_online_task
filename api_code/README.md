# comcom_online_task (API)
커먼컴퓨터 지원 온라인 과제


# Pellto's QnA API

## 사용법
1. [해당 레포지토리](https://github.com/pellto/comcom_online_task)를 다운로드 한 후 압축을 풀어 주세요.

2. move directory
```bash
cd api_code
```

3. API-server Build with Docker
```bash
docker build -t my-api-server:latest .
```

4. run api server with docker
```bash
docker run -d -p 5001:5001 --name my-api my-api-server:latest
```
and then wait about a minute (Downloading huggingface model)

5. Check Docker container running
```
docker ps
```

## API Parameter
- /QnA
  - post API
  - Use Fine-Tuned KoGPT-2 generater with [simple QnA Dataset](https://github.com/songys/Chatbot_data)
  - parameter :
    - input_text : Simple Question
<br>


# *with Swagger*
- [QnA Server](http://203.246.112.132:25001)
