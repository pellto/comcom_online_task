# comcom_online_task
커먼컴퓨터 지원 온라인 과제


## 사용법

1. Build Docker
```bash
docker build -t comcom .
```

2. Check Docker images
```bash
docker images
```
![image](https://user-images.githubusercontent.com/77001102/116267377-51504180-a7b7-11eb-8fc3-5620f8afe7e5.png)


3. Run Dokcer
```bash
docker dun -d -p 5000:5000 comcom
```
![image](https://user-images.githubusercontent.com/77001102/116267498-6c22b600-a7b7-11eb-9a75-b707062aa995.png)


4. Enter with Browser

127.0.0.1:5000
![image](https://user-images.githubusercontent.com/77001102/116267589-83fa3a00-a7b7-11eb-94b4-6d3e6f8b4eb4.png)


## Example
### Original KoGPT-2
- 허깅페이스의 KoGPT-2 모델을 이용해 만든 API를 사용해보는 곳
- 입력 문장 : 해당 문장을 기반으로 생성됩니다.
- 학습 모드 : 허깅페이스의 KoGPT-2의 generate parameter do_sample을 사용할 지 입력 받습니다.
- 문장 길이 : short / long 두개 중 하나를 입력으로 받습니다.
#### 예시
![image](https://user-images.githubusercontent.com/77001102/116268539-5feb2880-a7b8-11eb-91ea-1f1fefc9d6c4.png)

#### 결과
![image](https://user-images.githubusercontent.com/77001102/116268615-72656200-a7b8-11eb-9652-f541513a55c2.png)


### Simple QnA Service
- 허깅페이스의 KoGPT-2 모델을 [해당 데이터](https://github.com/songys/Chatbot_data)를 이용해 Fine-Tuning한 모델의 API를 사용할 수 있습니다.
- 단순 Question을 입력으로 받고, 단순 Answer를 출력을 보냅니다.
- Question : 물어볼 질문을 입력합니다.
- 출력 문장 : 출력 문장의 길이를 정합니다. (short / long)

#### 예시
- 입력 : 힘든 연애 좋은 연애라는게 무슨 차이일까? | 출력 : short


![image](https://user-images.githubusercontent.com/77001102/116269455-341c7280-a7b9-11eb-836a-622c01f20173.png)


### QnA ChatBot Service
- 허깅페이스의 KoGPT-2 모델을 [AI-HUB](https://aihub.or.kr/)에서 제공하는 [한국어 대화 데이터](https://aihub.or.kr/aidata/85/download)중 Dialog.zip 데이터를 이용해 Fine-Tuning한 모델의 API를 사용할 수 있습니다.
- 대화 데이터를 사용하여, 챗봇 서비스를 만들었습니다.
- 입력 : 어떠한 말을 해보세요.
- 출력 : 출력 문장의 길이 조건을 정합니다. (short / long)

#### 예시
- 입력 : 4인 가족이 먹으려면 라지 한 판으로 가능할까요? | 출력 : short


![image](https://user-images.githubusercontent.com/77001102/116270270-e8b69400-a7b9-11eb-91be-81e06830a517.png)

- 입력 : 아 그러면 그 콜라는 추가로 오나요? | 출력 : short


![image](https://user-images.githubusercontent.com/77001102/116270635-3cc17880-a7ba-11eb-89d5-661caf059ebf.png)


# API-Server
- check my [API Server](http://203.246.112.132:25000/)
