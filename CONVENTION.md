# Code Covention

### Naming
- class는 `pascal case`로 작성하고 다루고 있는 resource를 기준으로 명사로 사용한다.
```py
#example
class UserModel():
    pass
```
- 변수명이나 함수명은 `snake case`로 작성하고 함수명은 동사,변수명은 명사를 사용한다.
```py
#example
my_snake = "My Snake"
user = UserModel.set_name(my_snake)
```
- 할당 연산자는 가장 긴 변수명에 길이에 맞춘다.
```py
#example
first_num       = 1
second_num      = 2
third_num       = 3
one_hundred_num = 100
```

- 변수 할당 앞 뒤에 공백을 하나씩 추가한다.
- 괄호 안에서는 붙인다.

### Imports
- import는 한줄에 하나씩만 쓴다.
```py
#example
import os
import sys
import json
```
- python 내장 모듈/라이브러리, django framework에서 제공하는 모듈/라이브러리, 커스텀 모듈/라이브러리 순서로 작성한다.
- 가장 긴 path에 길이를 맞춘다.
```py
#example
import os
import sys
import json

from django.views     import View
from django.http      import HttpResponse
from django.db.models import Q

from users.models  import User, Admin
from boards.models import Board
```

# Branch Rule

### Reference
- https://nvie.com/posts/a-successful-git-branching-model/

### Summary
- 기본적으로 git flow 형식의 룰을 따른다.
- `main`, `develop`에는 직접 push하지 않는다.

### Branch
- `main` : 배포를 위한 브랜치.
- `develop` : 다음 버전 배포를 위해 개발하는 브랜치.
- `feature` : 기능 개발을 위한 브랜치.
- `hotfix` : `main`브랜치에서 발생한 버그를 수정하기 위한 브랜치.

# Commit Convention

### Reference
- https://doublesprogramming.tistory.com/256

### Summary
- 최대한 영어로만 작성
- 알기 쉽게 설명
- 작업 도중 다른 일이 생기거나 중단하게 될 경우 꼭 커밋을 작성하고 github에 push를 해놓는다(다른 사람이 이어서 작업하게 될 경우 바로 작업에 들어갈 수 있도록 하기 위해서)
- `rebase` 사용하기

### Type
- `feat` : 새로운 기능 추가
- `fix` : 버그 수정
- `docs` : 문서 수정
- `style` : 코드 포맷팅, 띄어쓰기, 들여쓰기
- `chore` : (코드 수정 없이) 빌드 스크립트 설정 변경, 패키지 매니저 수정
- `test` : 테스트 코드, 리팩토링 테스트 코드 추가
- `refactor` : 코드 리팩토링
- `merge` : merge 시 사용

### Example
- title : `fix: Add expried time in JWT from SignInView`
- content : `Add expired time in JWT from SignInView because of security and use datetime module to create expired time`

# PR Rule

- `기능 설명` : 어떤 기능을 개발했는지, 어떤 부분을 수정했는지 등
- `어려웠던 부분` : 기능 구현을 하면서 막혔거나, 어려웠던 부분 설명
- `issue number` : 이 PR이 몇번 issue인지 적는 부분
- label 꼭 확인하고 바꾸기
