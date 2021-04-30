# comcom_online_task
커먼컴퓨터 지원 온라인 과제

# 목차
1. [Demo](#Demo)
2. [My API Server](#My-API-Server)
3. [with Docker front and Docker API Server](#with-Docker-front-and-Docker-API-Server)
4. [with Docker front and My API Server](#with-Docker-front-and-My-API-Server)


## Demo
[Demo-Site](http://203.246.112.132:25000)

![image](https://user-images.githubusercontent.com/77001102/116668685-a1f2b500-a9d8-11eb-8cb5-474ed721fe72.png)



## My API Server
- check my [API Server](http://203.246.112.132:25001/)
- [Details](./api_code/README.md)


## with Docker front and Docker API Server
### 1. Build API-server
  1. move directory
  ```bash
  cd api_code
  ```

  2. API-server Build with Docker
  ```bash
  docker build -t my-api-server .
  ```

  3. run api server with docker
  ```bash
  docker run -d -p 5001:5001 --name my-api my-api-server
  ```
  and then wait about a minute (Downloading huggingface model)

  4. Check Docker container running
  ```
  docker ps
  ```
<br>


### 2. Build Front-server
  1. move directory (if you located in api-code directory)
  ```bash
  cd ..
  ```

  2. Front-server Build with Docker
  ```bash
  docker build -t my-front-server .
  ```

  3. run Front-Server and link API-Server with docker
  ```bash
  docker run -d -p 5000:5000 --link my-api:api my-front-server
  ```
  4. Check Docker container running
  ```
  docker ps
  ```

  5. enter with browser
  http://localhost:5000


## with Docker front and My API Server
- if My API Server Lived, then execute below
### 사용법

1. Modify POST_URL in main.py
from
```python
POST_URL = f"http://{os.environ['API_PORT_5001_TCP_ADDR']}:5001/QnA"
```
to
```python
POST_URL = f"http://203.246.112.132:5001/QnA"
```

2. Build Docker
```bash
docker build -t comcom .
```

3. Check Docker images
```bash
docker images
```
![image](https://user-images.githubusercontent.com/77001102/116267377-51504180-a7b7-11eb-8fc3-5620f8afe7e5.png)


4. Run Dokcer
```bash
docker dun -d -p 5000:5000 comcom
```
![image](https://user-images.githubusercontent.com/77001102/116267498-6c22b600-a7b7-11eb-9a75-b707062aa995.png)


5. Enter with Browser

http://localhost:5000
