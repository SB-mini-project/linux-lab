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
