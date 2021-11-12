# 🎊 Wanted X Wecode PreOnBoarding Backend Course | 무한루프 팀
원티드 2주차 기업 과제 : 8 Percent Assignment Project
  ✅ 8퍼센트 기업 과제입니다.
- [8퍼센트 사이트](https://8percent.kr/)
- [8퍼센트 채용공고 링크](https://www.wanted.co.kr/wd/64695) 


<br>
<br>

# 🔖 목차
- Team 소개
- 과제 내용
- 기술 환경 및 tools
- 모델링 ERD
- API 명세서
- 설치 및 실행 방법


<br>
<br>

# 🧑‍🤝‍🧑 Team 소개

| 이름 | 담당 기능 | 블로그 |
| :---: | :---: | :---: | 
| 공통 | 초기환경 설정, DB 모델링, postman api 문서 작성, README.md 작성, 배포, UnitTest | X |
| [유동헌](https://github.com/dhhyy) | 회원가입, 로그인 기능| |
| [하예준](https://github.com/TedJunny) | 거래내역 조회 기능 | |
| [오지윤(팀장)](https://github.com/Odreystella) | 출금 기능| |
| [손희정](https://github.com/heejung-gjt) | 입금 기능 |  |

<br>
<br>

# 📖 과제 내용    
> 계좌 거래 API를 구현해주세요. API는 3가지가 구현되어야 합니다.

### **[필수 포함 사항]**

- README 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - Swagger나 Postman을 통한 API 테스트할때 필요한 상세 방법
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

### **[개발 요구 사항]**
- 계좌의 잔액을 별도로 관리해야 하며, 계좌의 잔액과 거래내역의 잔액의 무결성의 보장
- DB를 설계 할때 각 칼럼의 타입과 제약   
- 거래내역 조회 API 
  - 아래와 같은 조회 화면에서 사용되는 API를 고려하시면 됩니다.     

  - 계좌의 소유주만 요청 할 수 있어야 합니다.
  - 거래일시에 대한 필터링이 가능해야 합니다.
  - 출금, 입금만 선택해서 필터링을 할 수 있어야 합니다.
  - Pagination이 필요 합니다.
  - 다음 사항이 응답에 포함되어야 합니다.
    - 거래일시
    - 거래금액
    - 잔액
    - 거래종류 (출금/입금)
    - 적요

- 입금 API
  - 계좌의 소유주만 요청 할 수 있어야 합니다.

- 출금 API
  - 계좌의 소유주만 요청 할 수 있어야 합니다.
  - 계좌의 잔액내에서만 출금 할 수 있어야 합니다. 잔액을 넘어선 출금 요청에 대해서는 적절한 에러처리가 되어야 합니다.

### **[가산점]**
- Unit test의 구현
- Functional Test 의 구현 (입금, 조회, 출금에 대한 시나리오 테스트)
- 거래내역이 1억건을 넘어갈 때에 대한 고려
    - 이를 고려하여 어떤 설계를 추가하셨는지를 README에 남겨 주세요.


### **[기능 개발]**

✔️ **REST API 기능**

- 거래내역 조회 API
- 입금 API
- 출금 API

<br>
<br>

# ➡️ Build(AWS EC2)
API URL : http://3.36.59.83:8000

<br>
<br>

# ⚒️ 기술 환경 및 tools
- Back-End: Python 3.9.7, Django 3.2.9
- Deploy: AWS EC2, Sqlite3 
- ETC: Git, Github, Postman

<br>
<br>

# 📋 모델링 ERD
[Aquerytool URL](https://aquerytool.com/aquerymain/index/?rurl=f82d6a29-7e62-4adc-b2db-1552d0ab617a&)     
Password : 0q7muv

![db](https://user-images.githubusercontent.com/64240637/141410518-862e73b1-fb57-4941-9895-2cc6366241b0.png)

<br>
<br>

# 🌲 디렉토리 구조
```
├── CONVENTION.md
├── PULL_REQUEST_TEMPLATE.md
├── README.md
├── config
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── db.sqlite3
├── my_settings.py
├── requirements.txt    
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── transactions
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── users
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

<br>
<br>

# 🔖 API 명세서
[Postman API Document 보러가기](https://documenter.getpostman.com/view/18212819/UVC8C6JT)

<br>

### 👉 회원가입/로그인
__유저에 해당하는 deposit과 transaction정보 등을 보기 위해서는 유저 회원가입/로그인 기능이 필요하다고 판단하였습니다.__   

[회원가입]

1. 유저 회원가입 시 이메일/패스워드/이름과 유저의 부가정보인 출금계좌/출금은행을 body에 담아 요청합니다.
2. 유저의 이메일과 패스워드 검증 후 유효하지 않을 경우 에러 메시지를 반환합니다.
3. 유효한 유저의 데이터인 경우 유저를 create합니다.

- Method: POST
```
http://3.37.8.131:8000/users/signup
```

- parameter : request_body
```
{
    "email"          : "gwangsu@gmail.com",
    "password"       : "2134234gneng!",
    "name"           : "지석진",
    "bank_name"      : "NH_BANK",
    "account_number" : "124239429421"
}
```
- response
```
{
    "message": "SUCCUESS"
}
```

[로그인]

1. 유저 로그인 시 이메일/패스워드를 body에 담아 요청합니다.
2. 유저의 이메일과 패스워드를 검증 후 유효하지 않는 경우 에러 메시지를 반환합니다.
3. 유효한 유저인 경우 유저의 token을 반환합니다.

- Method: POST
```
http://3.37.8.131:8000/users/signin
```

- parameter : request_body

```
{
    "email" : "gwangsu@gmail.com",
    "password" : "2134234gneng!"
}
```
- response
```
{
    "message": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozfQ.K-6qTURxJlk9W3kg0aeDmt4WJrVd11IiwrdNNvFOFkE"
}
```


### 👉 거래 내역 조회

1. 로그인 한 유저가 거래일시, 출금/입금 중 선택하여 요청합니다.
2. 로그인 한 유저의 유효성 검증 후 존재하지 않는 유저의 경우 에러 메시지를 반환합니다.
3. 유효한 유저의 경우 거래일시/거래금액/잔액/거래종류/적요 데이터를 offset limit 페이징 처리 후 반환합니다.

- Method: GET
```
http://3.37.8.131:8000/transactions/history?start_day=20210112
```

- header : Bearer token
- parameter : request_body

- response 

```
{
  "results": {
      "transactions": [
          {
              "created_time": "2021-11-12 21:20:03",
              "amounts": 3000,
              "balance": 30000,
              "information": "hello",
              "type": "입금"
          },
          {
              "created_time": "2021-11-12 21:19:46",
              "amounts": 10000,
              "balance": 27000,
              "information": "hello",
              "type": "출금"
          },
          {
              "created_time": "2021-11-12 21:19:30",
              "amounts": 3000,
              "balance": 37000,
              "information": "hello",
              "type": "출금"
          },
          {
              "created_time": "2021-11-12 21:07:29",
              "amounts": 8000,
              "balance": 40000,
              "information": "hello",
              "type": "입금"
          },
          {
              "created_time": "2021-11-12 21:03:34",
              "amounts": 8000,
              "balance": 32000,
              "information": "hello",
              "type": "입금"
          },
          {
              "created_time": "2021-11-12 21:00:29",
              "amounts": 8000,
              "balance": 24000,
              "information": "hello",
              "type": "입금"
          },
          {
              "created_time": "2021-11-12 20:59:23",
              "amounts": 8000,
              "balance": 16000,
              "information": "hello",
              "type": "입금"
          },
          {
              "created_time": "2021-11-12 20:58:52",
              "amounts": 8000,
              "balance": 8000,
              "information": "hello",
              "type": "입금"
          }
      ],
      "general_information": {
          "deposit_counts": 6,
          "deposit_sum_amounts": 43000,
          "withdrawal_counts": 2,
          "withdrawal_sum_amounts": 13000,
          "blance": 30000
        }
    }
}
```

### 👉 입금 

1. 입금할 금액과 적요를 body에 담아 요청합니다.
2. 금액의 타입이 Integer가 아닐 경우 TYPE_ERROR 메시지를 반환합니다.
3. 금액의 값이 음수일 경우 INVALID_ERROR 메시지를 반환합니다.
4. 키값이 올바르지 않을 경우 KEY_ERROR 메시지를 반환합니다.  
5. 요청이 성공적으로 처리된 후 성공 메시지를 반환합니다.

- Method: POST

```
http://3.37.8.131:8000/transactions/deposit
```

- header : Bearer token
- parameter : request_body


```
{
    "amounts": 10000,
    "information" : "입금"
}
```

- response
```
{
    "message": "Success",
    "user balance": 35000
}
```

### 👉 출금

1. 출금할 금액과 적요를 body에 담아 요청합니다.
2. 금액의 타입이 Integer가 아닐 경우 TYPE_ERROR 메시지를 반환합니다.
3. deposit balance에 있는 금액보다 출금할 금액이 더 클 경우 에러 메시지를 반환합니다.
4. 금액의 값이 음수일 경우 INVALID_INPUT 메시지를 반환합니다.
5. 키값이 올바르지 않을 경우 KEY_ERROR 메시지를 반환합니다.  
6. 요청이 성공적으로 처리된 후 성공 메시지를 반환합니다.

- Method: POST
```
http://3.37.8.131:8000/transactions/withdrawal
```

- header : Bearer token
- parameter : request_body


```
{
    "amounts": 10000,
    "information" : "출금"
}
```

- response   

```

```

<br>
<br>

# 🔖 설치 및 실행 방법

### 로컬 및 테스트용
1. 해당 프로젝트를 clone하고, 프로젝트로 들어간다.
```
git clone https://github.com/wanted-InfinityLoop/8percent-InfinityLoop.git .
cd 8percent
```

2. 가상환경으로 miniconda를 설치한다. [Go](https://docs.conda.io/en/latest/miniconda.html)

```
conda create -n wanted python=3.9
conda actvate 8percent
```   

3. 가상환경 생성 후, requirements.txt를 설치한다.

```
pip install -r requirements.txt

bcrypt==3.2.0
Django==3.2.9
django-cors-headers==3.10.0
PyJWT==2.3.0
gunicorn==20.1.0

```


4. migrate 후 로컬 서버 가동
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```



