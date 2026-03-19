TITLE = "YAML / JSON  (yq · jq)"

_YML  = "practice/data/docker-compose.yml"
_JSON = "practice/data/docker-compose.json"

QUESTIONS = [
    # ══════════════════════════════════════════════════════
    # Q1. YAML 유효성 검증 및 오류 수정  (그룹 3개)
    # ══════════════════════════════════════════════════════
    {
        "type": "group",
        "num": "1",
        "title": "YAML 파일 유효성 검증 및 오류 수정",
        "context": (
            f"파일: {_YML}\n"
            "위 파일에는 의도적인 YAML 들여쓰기 오류가 포함되어 있다.\n"
            "(nc_server 서비스의 environment 블록 내 '- TZ=UTC' 항목)"
        ),
        "subquestions": [
            {
                "id": "1-1",
                "type": "short",
                "q": "yq 명령어로 이 파일의 유효성을 검증하는 명령을 입력하라.",
                "practice_file": _YML,
                "hint": "yq [옵션] '.' 파일경로",
                "answer": f"yq -y '.' {_YML}",
                "acceptable": [
                    ["-y", ".", _YML.replace("practice/data/", "")],
                    ["yq", ".", _YML],
                ],
                "match_type": "multi",
                "explain": (
                    f"yq -y '.' {_YML}\n"
                    "  yq     : YAML Query — YAML 파싱/조회 도구\n"
                    "  -y     : 출력을 YAML 형식으로 유지\n"
                    "  '.'    : 전체 내용 출력 (identity 필터)\n"
                    "  오류가 있으면 파싱 에러 메시지 출력됨"
                ),
                "tip": "yq -y '.' 파일 → YAML 유효성 검증의 기본 패턴"
            },
            {
                "id": "1-2",
                "type": "short",
                "q": "오류를 수정(들여쓰기 교정)한 뒤 재검증하는 명령을 입력하라. (1-1과 동일 명령)",
                "practice_file": _YML,
                "hint": "1-1과 같은 명령어 — 파일 수정 후 다시 실행",
                "answer": f"yq -y '.' {_YML}",
                "acceptable": [
                    ["yq", ".", _YML.replace("practice/data/", "")],
                    ["yq", ".", "docker-compose.yml"],
                ],
                "match_type": "multi",
                "explain": (
                    "오류 수정: '- TZ=UTC' 앞 공백을 environment 하위 수준(6칸)으로 맞춤\n"
                    f"재검증: yq -y '.' {_YML}\n"
                    "  수정 후 동일 명령 실행 시 전체 YAML이 정상 출력되면 유효"
                ),
            },
            {
                "id": "1-3",
                "type": "short",
                "q": "수정된 파일에서 services.nc_server.restart 값을 읽어 출력하라.",
                "practice_file": _YML,
                "hint": "yq -y '.services.서비스명.키' 파일",
                "answer": f"yq -y '.services.nc_server.restart' {_YML}",
                "acceptable": [
                    ["yq", "nc_server.restart", "docker-compose.yml"],
                    ["yq", ".services.nc_server.restart"],
                ],
                "match_type": "multi",
                "explain": (
                    f"yq -y '.services.nc_server.restart' {_YML}\n"
                    "  중첩 키 접근: .상위키.중간키.하위키\n"
                    "  결과: unless-stopped\n"
                    "  ※ jq 문법과 동일하게 동작"
                ),
                "tip": "yq/jq 중첩 키: .a.b.c (점으로 계층 구분)"
            },
        ]
    },

    # ══════════════════════════════════════════════════════
    # Q2. 키 값 수정 후 다른 파일로 저장  (단일)
    # ══════════════════════════════════════════════════════
    {
        "type": "short",
        "num": "2",
        "q": "nc_server 서비스의 포트를 4432:443 → 8443:443 으로 변경하고 practice/data/custom.yml 로 저장하라.",
        "practice_file": _YML,
        "hint": "yq -y '.서비스.포트키 = [\"값\"]' 원본파일 > 저장파일",
        "answer": f"yq -y '.services.nc_server.ports = [\"8443:443\"]' {_YML} > practice/data/custom.yml",
        "acceptable": [
            ["yq", "nc_server.ports", "8443:443", "custom.yml"],
        ],
        "match_type": "multi",
        "explain": (
            f"yq -y '.services.nc_server.ports = [\"8443:443\"]' {_YML} > practice/data/custom.yml\n"
            "  .services.nc_server.ports = [...] : 배열 값 덮어쓰기\n"
            "  > custom.yml : 결과를 새 파일로 리다이렉션\n"
            "  ※ -i 옵션은 원본 파일 직접 수정 (In-place)"
        ),
        "tip": "yq 값 변경: '.키 = 값' / 저장: > 파일  or  -i (In-place)"
    },

    # ══════════════════════════════════════════════════════
    # Q3. YAML → JSON 변환  (그룹 3개)
    # ══════════════════════════════════════════════════════
    {
        "type": "group",
        "num": "3",
        "title": "YAML → JSON 변환",
        "context": (
            f"파일: {_YML}\n"
            "위 YAML 파일을 JSON 형식으로 변환하고 검증해야 한다."
        ),
        "subquestions": [
            {
                "id": "3-1",
                "type": "short",
                "q": "yq를 사용해 docker-compose.yml을 JSON 형식으로 출력하라. (-y 옵션 없이)",
                "practice_file": _YML,
                "hint": "yq (옵션없이) '.' 파일  →  기본 출력이 JSON",
                "answer": f"yq '.' {_YML}",
                "acceptable": [
                    ["yq", ".", "docker-compose.yml"],
                    ["yq '.' practice/data/docker-compose.yml"],
                ],
                "match_type": "multi",
                "explain": (
                    f"yq '.' {_YML}\n"
                    "  -y 없이 실행하면 yq의 기본 출력은 JSON 형식\n"
                    "  -y 붙이면 YAML 형식으로 출력"
                ),
                "tip": "yq 기본출력=JSON / yq -y 출력=YAML"
            },
            {
                "id": "3-2",
                "type": "short",
                "q": "출력된 JSON을 practice/data/docker-compose.json 파일로 저장하라.",
                "practice_file": _YML,
                "hint": "yq '.' 파일 > 저장경로",
                "answer": f"yq '.' {_YML} > {_JSON}",
                "acceptable": [
                    ["yq", ".", "docker-compose.yml", ">", "docker-compose.json"],
                    ["yq", "docker-compose.yml", ">", ".json"],
                ],
                "match_type": "multi",
                "explain": (
                    f"yq '.' {_YML} > {_JSON}\n"
                    "  > : 표준 출력을 파일로 리다이렉션\n"
                    "  결과: JSON 형식의 docker-compose.json 생성"
                ),
            },
            {
                "id": "3-3",
                "type": "short",
                "q": "저장된 docker-compose.json이 유효한 JSON인지 jq로 검증하라.",
                "practice_file": _JSON,
                "hint": "jq '.' 파일  →  유효하면 전체 JSON 출력",
                "answer": f"jq '.' {_JSON}",
                "acceptable": [
                    ["jq", ".", "docker-compose.json"],
                ],
                "match_type": "multi",
                "explain": (
                    f"jq '.' {_JSON}\n"
                    "  jq    : JSON Query — JSON 파싱/조회 도구\n"
                    "  '.'   : identity 필터 (전체 출력)\n"
                    "  정상이면 전체 JSON 출력 / 오류 시 parse error 출력"
                ),
                "tip": "jq/yq 모두 '.' 필터가 유효성 검증의 기본 패턴"
            },
        ]
    },

    # ══════════════════════════════════════════════════════
    # Q4. 특정 환경변수 항목 삭제  (그룹 4개)
    # ══════════════════════════════════════════════════════
    {
        "type": "group",
        "num": "4",
        "title": "YAML 특정 환경변수 항목 삭제",
        "context": (
            f"파일: {_JSON}  (Q3에서 생성한 JSON)\n"
            "nc_mariadb의 environment 배열에서\n"
            "MYSQL_ROOT_PASSWORD 항목을 삭제해야 한다."
        ),
        "subquestions": [
            {
                "id": "4-1",
                "type": "short",
                "q": "jq로 nc_mariadb 서비스의 environment 배열 전체를 출력하라.",
                "practice_file": _JSON,
                "hint": "jq '.services.서비스명.environment' 파일",
                "answer": f"jq '.services.nc_mariadb.environment' {_JSON}",
                "acceptable": [
                    ["jq", "nc_mariadb.environment", "docker-compose.json"],
                ],
                "match_type": "multi",
                "explain": (
                    f"jq '.services.nc_mariadb.environment' {_JSON}\n"
                    "  배열 전체 출력 → 각 항목의 인덱스(0부터) 확인 가능\n"
                    "  MYSQL_ROOT_PASSWORD 는 인덱스 [3] 에 위치"
                ),
            },
            {
                "id": "4-2",
                "type": "short",
                "q": "인덱스 3을 지정하여 MYSQL_ROOT_PASSWORD를 삭제한 결과를 화면에만 출력하라. (파일 수정 없이)",
                "practice_file": _JSON,
                "hint": "jq 'del(.서비스.환경변수[인덱스])' 파일",
                "answer": f"jq 'del(.services.nc_mariadb.environment[3])' {_JSON}",
                "acceptable": [
                    ["jq", "del", "nc_mariadb.environment[3]", "docker-compose.json"],
                ],
                "match_type": "multi",
                "explain": (
                    f"jq 'del(.services.nc_mariadb.environment[3])' {_JSON}\n"
                    "  del() : 지정한 경로의 요소를 삭제하는 jq 내장 함수\n"
                    "  [3]   : 0-based 인덱스 → 4번째 항목\n"
                    "  리다이렉션 없이 실행 → 화면 출력만, 파일 변경 없음"
                ),
                "tip": "jq del(): 삭제 / jq += []: 추가 — 파일 변경은 > 리다이렉션 필요"
            },
            {
                "id": "4-3",
                "type": "short",
                "q": "삭제 결과를 docker-compose.json 파일에 직접 반영하라.",
                "practice_file": _JSON,
                "hint": "jq 'del(...)' 파일 > 임시파일 && mv 임시파일 원본파일",
                "answer": f"jq 'del(.services.nc_mariadb.environment[3])' {_JSON} > practice/data/tmp.json && mv practice/data/tmp.json {_JSON}",
                "acceptable": [
                    ["del", "environment[3]", ">", "tmp.json", "mv", "docker-compose.json"],
                    ["del", "environment[3]", ">", ".json", "mv"],
                ],
                "match_type": "multi",
                "explain": (
                    "jq는 파일 직접 수정(-i) 옵션이 없으므로 임시 파일 경유:\n"
                    f"  1) jq 'del(...)' {_JSON} > practice/data/tmp.json\n"
                    "  2) mv practice/data/tmp.json {_JSON}\n"
                    "  또는 && 로 한 줄로 연결"
                ),
            },
            {
                "id": "4-4",
                "type": "short",
                "q": "반영 후 environment 목록을 출력하여 항목이 삭제되었는지 확인하라.",
                "practice_file": _JSON,
                "hint": "4-1과 동일한 명령어",
                "answer": f"jq '.services.nc_mariadb.environment' {_JSON}",
                "acceptable": [
                    ["jq", "nc_mariadb.environment", "docker-compose.json"],
                ],
                "match_type": "multi",
                "explain": (
                    f"jq '.services.nc_mariadb.environment' {_JSON}\n"
                    "  삭제 전: 7개 항목\n"
                    "  삭제 후: 6개 항목 (MYSQL_ROOT_PASSWORD 없음)\n"
                    "  4-1과 동일 명령 — 전후 결과를 비교하는 것이 포인트"
                ),
            },
        ]
    },

    # ══════════════════════════════════════════════════════
    # Q5. 배열에 환경변수 추가  (객관식)
    # ══════════════════════════════════════════════════════
    {
        "type": "mcq",
        "num": "5",
        "q": "nc_redis의 environment 배열에 'UMASK=022' 항목을 추가하는 올바른 jq 명령은?",
        "practice_file": _JSON,
        "options": [
            "① jq 'del(.services.nc_redis.environment[] | \"UMASK=022\")' docker-compose.json",
            "② jq 'add(.services.nc_redis.environment, \"UMASK=022\")' docker-compose.json",
            "③ jq '.services.nc_redis.environment += [\"UMASK=022\"]' docker-compose.json",
            "④ jq '.services.nc_redis.environment[4] | \"UMASK=022\"' docker-compose.json",
        ],
        "answer": 3,
        "explain": (
            "③ += 연산자로 배열에 새 항목을 추가 → 정답\n"
            "\n"
            "  ① del() : 삭제 함수 — 추가와 무관\n"
            "  ② add() : jq에 존재하지 않는 문법\n"
            "  ③ += [\"값\"] : 배열 끝에 항목 추가 ✅\n"
            "  ④ | : 파이프는 필터링/전달 — 추가 기능 없음"
        ),
        "tip": "jq 배열 추가: .배열 += [\"값\"] / 삭제: del(.배열[N])"
    },
]
