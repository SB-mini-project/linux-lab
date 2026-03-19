TITLE = "grep / awk / find"

# ──────────────────────────────────────────────────────────────────────
# 필드 구조 (access.log):
#   $1=IP  $2=날짜  $3=시간  $4=상태코드  $5=바이트  $6=메서드  $7=경로
#
# 필드 구조 (secure.log):
#   $1=날짜 $2=시간 $3=서버 $4=서비스 $5=PID $6=모듈 $7=세션
#   $8=auth $9=FAILED/SUCCESS $10=for $11=유저명 $12=from $13=IP
# ──────────────────────────────────────────────────────────────────────

QUESTIONS = [
    # ── Q1 객관식 ─────────────────────────────────────────
    {
        "type": "mcq",
        "num": "1",
        "q": "error_202603.log에서 ERROR 또는 WARN을 대소문자 구분 없이 찾는 명령은?",
        "practice_file": "practice/logs/error_202603.log",
        "options": [
            "① grep -E \"ERROR|WARN\" error_202603.log",
            "② grep -i \"ERROR|WARN\" error_202603.log",
            "③ grep -i -E \"ERROR|WARN\" error_202603.log",
            "④ grep -v \"ERROR|WARN\" error_202603.log",
        ],
        "answer": 3,
        "explain": (
            "-E (Extended regex) : 확장 정규식 → | (OR) 사용 가능\n"
            "  -i (Ignore case)    : 대소문자 구분 없이 검색\n"
            "  둘 다 필요 → -i -E 조합이 정답\n"
            "  ① -E만 쓰면 대소문자 구분 O\n"
            "  ② -i만 쓰면 | 가 리터럴 문자로 처리됨\n"
            "  ④ -v (inVert): 매칭 제외 줄 출력"
        ),
        "tip": "-E = Extended(확장정규식), -i = Ignore case, 동시 사용 가능"
    },

    # ── Q2 객관식 ─────────────────────────────────────────
    {
        "type": "mcq",
        "num": "2",
        "q": "access.log에서 상태코드($4)가 500인 행만 출력하는 awk 조건으로 옳은 것은?",
        "practice_file": "practice/logs/access.log  ($4 = 4번째 필드 = 상태코드)",
        "options": [
            "① awk '$4 = 500 {print}' access.log",
            "② awk '$4 == 500 {print}' access.log",
            "③ awk '$4 != 500 {print}' access.log",
            "④ awk '{if $4 == 500}' access.log",
        ],
        "answer": 2,
        "explain": (
            "== : 비교 연산자 → 정답\n"
            "  =  : 대입 연산자 (비교 아님!)\n"
            "  != : 같지 않을 때 (부정)\n"
            "  ④ : awk if 문법 오류 → if($4==500){print} 이 올바른 형태"
        ),
        "tip": "awk 비교: == / 대입: = / 부정: != — SQL과 동일"
    },

    # ── Q3 주관식 ─────────────────────────────────────────
    {
        "type": "short",
        "num": "3",
        "q": "현재 디렉터리 아래에서 .log 파일만 찾아, 그 안에 'timeout' 문자열이 포함된 줄을 검색하시오.",
        "practice_file": "practice/logs/  (error_202603.log에 timeout 포함)",
        "hint": "find . -name '*.log' -exec grep '패턴' {} 종료기호",
        "answer": "find . -name '*.log' -exec grep 'timeout' {} \\;",
        "acceptable": [
            "find . -name '*.log' -exec grep 'timeout' {} \\;",
            "find . -name \"*.log\" -exec grep 'timeout' {} \\;",
            "find . -name '*.log' -exec grep timeout {} \\;",
            "find . -name '*.log' -exec grep \"timeout\" {} \\;",
            ["find", "*.log", "exec", "grep", "timeout"],
        ],
        "match_type": "multi",
        "explain": (
            "find . -name '*.log' -exec grep 'timeout' {} \\;\n"
            "  -name '*.log'  : 이름이 .log 로 끝나는 파일\n"
            "  -exec CMD {} \\; : 찾은 파일 각각에 CMD 실행\n"
            "  {}             : find가 찾은 파일명 자리\n"
            "  \\;            : -exec 블록 종료 구분자"
        ),
        "tip": "find -exec {} \\; 패턴 암기! {}=파일자리, \\;=끝"
    },

    # ── Q4 주관식 ─────────────────────────────────────────
    {
        "type": "short",
        "num": "4",
        "q": "access.log에서 요청 방식($6)이 POST인 줄의 IP($1)와 경로($7)를 출력하시오.",
        "practice_file": "practice/logs/access.log",
        "hint": "awk '$필드==\"값\" {print $N, $M}' 파일",
        "answer": "awk '$6==\"POST\" {print $1, $7}' logs/access.log",
        "acceptable": [
            ['$6=="post"', "print $1", "$7", "access.log"],
            ['$6==\'post\'', "print $1", "$7", "access.log"],
        ],
        "match_type": "multi",
        "explain": (
            "awk '$6==\"POST\" {print $1, $7}' logs/access.log\n"
            "  $6==\"POST\" : 6번째 필드(메서드)가 POST인 줄 필터\n"
            "  {print $1, $7} : 1번째(IP)와 7번째(경로) 출력\n"
            "\n"
            "  access.log 필드 구조:\n"
            "  $1=IP  $2=날짜  $3=시간  $4=상태코드  $5=바이트  $6=메서드  $7=경로"
        ),
        "tip": "awk 문자열 비교: $N==\"값\" (== 양쪽 공백 없이)"
    },

    # ── Q5 주관식 ─────────────────────────────────────────
    {
        "type": "short",
        "num": "5",
        "q": "secure.log에서 로그인 결과($9)가 FAILED이면 유저명($11)과 '실패'를, 아니면 유저명과 '성공'을 출력하시오.",
        "practice_file": "practice/logs/secure.log  ($9=결과, $11=유저명)",
        "hint": "awk '{if($9==\"FAILED\") print $11, \"실패\"; else print $11, \"성공\"}' 파일",
        "answer": "awk '{if($9==\"FAILED\") print $11, \"실패\"; else print $11, \"성공\"}' logs/secure.log",
        "acceptable": [
            ["if($9", "failed", "print $11", "실패", "성공", "secure.log"],
        ],
        "match_type": "multi",
        "explain": (
            "awk '{if($9==\"FAILED\") print $11, \"실패\"; else print $11, \"성공\"}' logs/secure.log\n"
            "\n"
            "  if (조건) 실행문; else 실행문  — awk 조건 분기\n"
            "  $9  : SUCCESS 또는 FAILED\n"
            "  $11 : 유저명 (user1, admin1 등)\n"
            "\n"
            "  secure.log 필드:\n"
            "  $1=날짜 $2=시간 $3=서버 $4=서비스 $5=PID\n"
            "  $6=모듈 $7=세션 $8=auth $9=결과 $10=for $11=유저명"
        ),
        "tip": "awk if/else: '{if(조건) A; else B}' — 세미콜론으로 구분"
    },
]
