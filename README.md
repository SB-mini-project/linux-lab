# 🐧 LINUX LAB — Sangam Beavers

Linux 명령어 실습 퀴즈 CLI 프로그램

## 📋 카테고리

| 번호 | 주제 | 문제 수 | 형식 |
|------|------|---------|------|
| 1 | grep / awk / find | 5문제 | 객관식 2 + 주관식 3 |
| 2 | YAML / JSON (yq · jq) | 12문제 | 그룹/객관식/주관식 혼합 |
| 3 | 환경 초기화 | - | practice/ 복원 |

## ⚙️ 설치

```bash
git clone https://github.com/yourname/linux-lab.git
cd linux-lab
chmod +x install.sh
sudo ./install.sh

# 실행
linux-lab

# 또는 설치 없이
python3 quiz.py
```

**요구사항**: Python 3.7+  |  외부 라이브러리 없음

## 🗂️ 파일 구조

```
linux-lab/
├── quiz.py                        # 메인 실행 파일
├── core/
│   ├── engine.py                  # 퀴즈 엔진 (객관식/주관식/그룹)
│   └── reset.py                   # 환경 초기화
├── questions/
│   ├── grep_awk_find.py           # 1번 카테고리
│   └── yaml_json.py               # 2번 카테고리
├── practice/
│   ├── logs/
│   │   ├── access.log             # 웹 접근 로그 (grep/awk 실습)
│   │   ├── error_202603.log       # 에러 로그 (grep 실습)
│   │   └── secure.log             # 인증 로그 (awk 실습)
│   └── data/
│       ├── docker-compose.yml     # 오류 포함 YAML (yq 실습)
│       ├── user_list.csv          # 사용자 목록
│       └── server_info.tsv        # 서버 정보
├── install.sh
├── .gitignore
└── README.md
```

## 🧪 실습 파일 필드 구조

**access.log** (공백 구분)
```
$1=IP  $2=날짜  $3=시간  $4=상태코드  $5=바이트  $6=메서드  $7=경로
192.168.0.2 2026-03-01 08:15:00 500 512 POST /login
```

**secure.log** (공백 구분)
```
$1=날짜  $2=시간  $3=서버  $4=서비스  $5=PID  $6=모듈
$7=세션  $8=auth  $9=결과(SUCCESS/FAILED)  $10=for  $11=유저명
```

## ➕ 문제 추가 방법

`questions/` 폴더 파일에 아래 형식으로 추가:

```python
# 객관식
{
    "type": "mcq",
    "num": "6",
    "q": "문제 내용",
    "options": ["① ...", "② ...", "③ ...", "④ ..."],
    "answer": 2,
    "explain": "해설",
    "tip": "암기팁"    # 선택
}

# 주관식
{
    "type": "short",
    "num": "7",
    "q": "문제 내용",
    "hint": "힌트",    # 선택
    "answer": "정답 명령어",
    "acceptable": [    # 허용 답안 목록 (키워드 리스트도 가능)
        ["키워드1", "키워드2", "키워드3"],
    ],
    "match_type": "multi",   # exact / contains / multi
    "explain": "해설",
}

# 그룹 (서브문제 묶음)
{
    "type": "group",
    "num": "8",
    "title": "그룹 제목",
    "context": "배경 설명",
    "subquestions": [
        {"id": "8-1", "type": "short", "q": "...", ...},
        {"id": "8-2", "type": "mcq",   "q": "...", ...},
    ]
}
```

## 📝 License

MIT

# Question & Answer

## 1번: YAML 파일 유효성 검증 및 오류 수정

### Q.

* 의도적으로 오류가 포함된 YAML 파일 `/data/docker-compose.yml`이다. 오류 메시지를 확인하고, 오류를 직접 수정한 뒤 다시 검증하라.

### A.

* **에러 분석**: 에러 메시지의 "line 15, column 6"은 오류가 감지된 위치입니다. 실제 원인은 YAML의 블록 매핑 문법을 파싱할 때 line 4에서 시작된 구조에서 예상한 키가 line 15에서 발견되지 않았다는 의미입니다. 이는 보통 들여쓰기가 규칙과 맞지 않을 때 발생합니다.

* **수정 방법**: 

    1. 15번째 줄 근처의 들여쓰기를 확인합니다 (YAML은 스페이스 또는 탭 혼용 금지)

    2. line 4-15 사이의 들여쓰기 일관성을 검토합니다

    3. 수정 후 다시 검증합니다

    ```bash
    yq -y '.' /data/docker-compose.yml
    ```

## 2번: 키 값 수정 후 다른 파일로 저장

### Q.

* `nc_server` 서비스의 포트를 `4432:443` → `8443:443` 으로 변경하라. 결과를 `/data/custom.yml`로 저장하라.

### A.

* 할당 연산자 `=`를 사용하여 ports 값을 배열 형식 `["8443:443"]`으로 변경합니다. 원본 파일은 수정되지 않고, 결과를 리다이렉트(>)로 새 파일에 저장합니다.

    ```bash
    yq -y '.services.nc_server.ports = ["8443:443"]' /data/docker-compose.yml > /data/custom.yml
    ```

## 3번: YAML → JSON 변환

### Q.

* `/data/docker-compose.yml` 전체를 JSON 형식으로 변환해야 한다. 변환된 JSON을 `/data/docker-compose.json` 파일로 저장하라.

### A.

* `-y` 옵션 없이 기본 출력 형식(JSON)으로 변환하고, 결과를 docker-compose.json 파일로 저장합니다. yq는 기본적으로 JSON으로 출력하기 때문에 이를 파일로 저장하면 JSON 형식의 파일이 됩니다.

    ```bash
    yq '.' /data/docker-compose.yml > /data/docker-compose.json
    ```

## 4번: YAML 특정 환경변수 항목 삭제

### Q.

* `/data/docker-compose.json` 파일의 `nc_mariadb` 서비스에는 아래와 같은 환경변수들이 정의되어 있다.

    ```
    environment:
    - PUID=${OPR_UID}
    - PGID=${OPR_GID}
    - TZ=UTC
    - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
    - MYSQL_DATABASE=${DB_NAME}
    - MYSQL_USER=${DB_USER}
    - MYSQL_PASSWORD=${DB_PASSWORD}
    ```

* 보안 정책에 따라 `MYSQL_ROOT_PASSWORD` 항목을 환경변수 목록에서 제거하시오.

### A.

* `del()` 함수를 사용하여 `MYSQL_ROOT_PASSWORD` 항목이 포함된 배열 요소를 삭제합니다. 배열 요소는 0부터 시작하는 인덱스로 접근하므로, `MYSQL_ROOT_PASSWORD`가 4번째 요소라면 인덱스는 3입니다. 결과를 임시 파일로 저장한 후 원본 파일로 덮어씁니다.

    ```bash
    jq 'del(.services.nc_mariadb.environment[3])' /data/docker-compose.json > /data/tmp.json
    mv /data/tmp.json /data/docker-compose.json
    ```

## 5번: JSON 배열에 환경변수 항목 추가

### Q.

* `/data/docker-compose.json` 파일의 `nc_redis` 서비스의 `environment` 배열에 `- UMASK=022` 항목을 추가하려고 한다. 올바른 명령어를 고르시오.

  1.`jq 'del(.services.nc_redis.environment[] | "UMASK=022")' /data/docker-compose.json` 

  2.`jq 'add(.services.nc_redis.environment, "UMASK=022")' /data/docker-compose.json`

  3.`jq '.services.nc_redis.environment += ["UMASK=022"]' /data/docker-compose.json`

  4.`jq '.services.nc_redis.environment[4] | "UMASK=022"' /data/docker-compose.json`

### A.

| 보기 | 설명 | 평가 |
| --- | --- | --- |
| 1. | `del()`은 배열 요소를 **삭제**하는 함수로, 추가와는 관계 없음 | ❌ |
| 2. | `add()`는 jq/yq에서 **배열 병합** 등에 사용되는 함수이지만, 단순 요소 추가에는 부적합 | ❌ |
| 3. | `+=` 연산자는 배열에 새 요소를 **올바르게 추가**하는 방법 | ✅ **정답** |
| 4. | `\|` 파이프는 필터를 연결하여 데이터를 변환할 뿐, 배열 추가 기능 없음 | ❌ |
