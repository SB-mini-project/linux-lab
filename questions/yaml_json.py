TITLE = "YAML / JSON  (yq · jq)"

_YML  = "practice/data/docker-compose.yml"
_JSON = "practice/data/docker-compose.json"

# 새 docker-compose 오류 위치:
#   nc_server > environment 블록에서
#   '    - PGID=${OPR_GID}' 의 들여쓰기가 4칸 → 6칸이어야 함

QUESTIONS = [
    # ── Q1 주관식 ─────────────────────────────────────────
    {
        "type": "short",
        "num": "1",
        "q": "오류가 포함된 docker-compose.yml의 유효성을 yq로 검증하는 명령을 입력하라.",
        "practice_file": _YML + "  ← nc_server environment 블록에 들여쓰기 오류 있음",
        "hint": "yq [옵션] '.' 파일경로  |  YAML 형식 유지 옵션: -y",
        "answer": "yq -y '.' practice/data/docker-compose.yml",
        "acceptable": [
            ["yq", "-y", ".", "docker-compose.yml"],
            ["yq", "-y", ".", _YML],
            ["yq", ".", "docker-compose.yml"],
        ],
        "match_type": "multi",
        "explain": (
            "yq -y '.' practice/data/docker-compose.yml\n"
            "\n"
            "  yq  : YAML Query — YAML 파싱/조회 도구\n"
            "  -y  : 출력을 YAML 형식으로 유지 (없으면 JSON 출력)\n"
            "  '.' : identity 필터 — 전체 내용 그대로 출력\n"
            "\n"
            "  오류가 있으면 아래와 같은 메시지 출력:\n"
            "  ParserError: did not find expected key\n"
            "    → nc_server > environment 의 '- PGID' 들여쓰기 오류\n"
            "  수정: 4칸 → 6칸으로 맞춰야 함"
        ),
        "tip": "yq -y '.' 파일 → YAML 유효성 검증의 기본 패턴"
    },

    # ── Q2 주관식 ─────────────────────────────────────────
    {
        "type": "short",
        "num": "2",
        "q": "nc_server 서비스의 포트를 4432:443 → 8443:443 으로 변경하고 practice/data/custom.yml 로 저장하라.",
        "practice_file": _YML,
        "hint": "yq -y '.services.서비스.ports = [\"값\"]' 원본 > 저장파일",
        "answer": "yq -y '.services.nc_server.ports = [\"8443:443\"]' practice/data/docker-compose.yml > practice/data/custom.yml",
        "acceptable": [
            ["yq", "nc_server.ports", "8443:443", ">", "custom.yml"],
            ["yq", "nc_server", "8443", ">", ".yml"],
        ],
        "match_type": "multi",
        "explain": (
            "yq -y '.services.nc_server.ports = [\"8443:443\"]' practice/data/docker-compose.yml > practice/data/custom.yml\n"
            "\n"
            "  .services.nc_server.ports = [...] : ports 값을 배열로 덮어쓰기\n"
            "  > custom.yml : 결과를 새 파일로 리다이렉션\n"
            "  원본 파일은 수정되지 않음\n"
            "  ※ 원본 직접 수정하려면 -i (In-place) 옵션 사용"
        ),
        "tip": "yq 값 변경: '.키 = 값'  |  새 파일 저장: > 파일  |  원본 수정: -i"
    },

    # ── Q3 주관식 ─────────────────────────────────────────
    {
        "type": "short",
        "num": "3",
        "q": "docker-compose.yml 전체를 JSON으로 변환해 practice/data/docker-compose.json 으로 저장하라.",
        "practice_file": _YML,
        "hint": "yq (옵션 없이) '.' 파일 > 저장경로  |  기본 출력이 JSON",
        "answer": "yq '.' practice/data/docker-compose.yml > practice/data/docker-compose.json",
        "acceptable": [
            ["yq", ".", "docker-compose.yml", ">", "docker-compose.json"],
            ["yq", "docker-compose.yml", ">", ".json"],
        ],
        "match_type": "multi",
        "explain": (
            "yq '.' practice/data/docker-compose.yml > practice/data/docker-compose.json\n"
            "\n"
            "  -y 없이 실행 → yq 기본 출력은 JSON 형식\n"
            "  -y 붙이면   → YAML 형식으로 출력\n"
            "  > docker-compose.json : 결과를 JSON 파일로 저장\n"
            "\n"
            "  저장 후 jq로 검증:\n"
            "  jq '.' practice/data/docker-compose.json"
        ),
        "tip": "yq 기본출력=JSON  /  yq -y 출력=YAML"
    },

    # ── Q4 주관식 ─────────────────────────────────────────
    {
        "type": "short",
        "num": "4",
        "q": "docker-compose.json의 nc_mariadb environment에서 MYSQL_ROOT_PASSWORD 항목(인덱스 3)을 삭제하고 파일에 반영하라.",
        "practice_file": _JSON + "  ← Q3 실행 후 생성됨",
        "hint": "jq 'del(.services.서비스.environment[N])' 파일 > 임시파일 && mv 임시파일 원본",
        "answer": "jq 'del(.services.nc_mariadb.environment[3])' practice/data/docker-compose.json > practice/data/tmp.json && mv practice/data/tmp.json practice/data/docker-compose.json",
        "acceptable": [
            ["del", "nc_mariadb.environment[3]", ">", "tmp.json", "mv"],
            ["del", "environment[3]", ">", ".json", "mv"],
        ],
        "match_type": "multi",
        "explain": (
            "jq 'del(.services.nc_mariadb.environment[3])' practice/data/docker-compose.json > practice/data/tmp.json\n"
            "mv practice/data/tmp.json practice/data/docker-compose.json\n"
            "\n"
            "  del()  : 지정한 경로의 요소를 삭제하는 jq 내장 함수\n"
            "  [3]    : 0-based 인덱스 → 4번째 항목 (MYSQL_ROOT_PASSWORD)\n"
            "\n"
            "  environment 인덱스:\n"
            "    [0] PUID  [1] PGID  [2] TZ  [3] MYSQL_ROOT_PASSWORD\n"
            "    [4] MYSQL_DATABASE  [5] MYSQL_USER  [6] MYSQL_PASSWORD\n"
            "\n"
            "  jq는 -i 옵션 없음 → 임시파일 경유 후 mv 로 덮어씀"
        ),
        "tip": "jq 파일 수정: > tmp.json && mv tmp.json 원본  (jq는 -i 없음!)"
    },

    # ── Q5 객관식 ─────────────────────────────────────────
    {
        "type": "mcq",
        "num": "5",
        "q": "nc_redis의 environment 배열에 'UMASK=022' 항목을 추가하는 올바른 jq 명령은?",
        "practice_file": _JSON,
        "options": [
            '① jq \'del(.services.nc_redis.environment[] | "UMASK=022")\' docker-compose.json',
            '② jq \'add(.services.nc_redis.environment, "UMASK=022")\' docker-compose.json',
            '③ jq \'.services.nc_redis.environment += ["UMASK=022"]\' docker-compose.json',
            '④ jq \'.services.nc_redis.environment[4] | "UMASK=022"\' docker-compose.json',
        ],
        "answer": 3,
        "explain": (
            "① del()   : 삭제 함수 — 추가와 무관                       ❌\n"
            "  ② add()   : jq에 존재하지 않는 문법                        ❌\n"
            "  ③ += [값] : 배열 끝에 새 항목을 올바르게 추가              ✅\n"
            "  ④ |       : 파이프는 필터 연결 — 배열 추가 기능 없음        ❌"
        ),
        "tip": "jq 배열 추가: .배열 += [\"값\"]  |  삭제: del(.배열[N])"
    },
]
