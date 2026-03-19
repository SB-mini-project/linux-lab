#!/usr/bin/env python3
"""
LINUX LAB - SANGAM BEAVERS
CLI 문제 풀이 프로그램

사용법:
  python3 quiz.py
  또는 (설치 후)
  linux-lab
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine import C, c, divider, safe_input, show_score

# ── 배너 ────────────────────────────────────────────────

BANNER = """\033[97m
  ██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗    ██╗      █████╗ ██████╗
  ██║     ██║████╗  ██║██║   ██║╚██╗██╔╝    ██║     ██╔══██╗██╔══██╗
  ██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝     ██║     ███████║██████╔╝
  ██║     ██║██║╚██╗██║██║   ██║ ██╔██╗     ██║     ██╔══██║██╔══██╗
  ███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗    ███████╗██║  ██║██████╔╝
  ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚═════╝
\033[0m\033[90m  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\033[0m\033[97m
  ███████╗ █████╗ ███╗   ██╗ ██████╗  █████╗ ███╗   ███╗
  ██╔════╝██╔══██╗████╗  ██║██╔════╝ ██╔══██╗████╗ ████║
  ███████╗███████║██╔██╗ ██║██║  ███╗███████║██╔████╔██║
  ╚════██║██╔══██║██║╚██╗██║██║   ██║██╔══██║██║╚██╔╝██║
  ███████║██║  ██║██║ ╚████║╚██████╔╝██║  ██║██║ ╚═╝ ██║
  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝
\033[0m\033[90m  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\033[0m\033[97m
  ██████╗ ███████╗ █████╗ ██╗   ██╗███████╗██████╗ ███████╗
  ██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗██╔════╝
  ██████╔╝█████╗  ███████║██║   ██║█████╗  ██████╔╝███████╗
  ██╔══██╗██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║
  ██████╔╝███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║███████║
  ╚═════╝ ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝
\033[0m"""

MENU = """\
  ┌──────────────────────────────────────────────┐
  │              📋  카테고리 선택               │
  ├──────────────────────────────────────────────┤
  │   1  │  grep / awk / find          (5문제)   │
  │   2  │  YAML / JSON  (yq · jq)    (12문제)   │
  ├──────────────────────────────────────────────┤
  │   3  │  🔄 실습 환경 초기화                  │
  ├──────────────────────────────────────────────┤
  │  exit │  프로그램 종료                       │
  └──────────────────────────────────────────────┘"""

def show_banner():
    os.system("clear" if os.name == "posix" else "cls")
    print(BANNER)

def do_reset():
    from core.reset import reset_practice, PRACTICE
    print()
    print(c(C.YELLOW, "  ⚠  practice/ 디렉터리를 초기 상태로 복원합니다."))
    ans = safe_input(c(C.WHITE, "  계속하시겠습니까? (y/N) ▶ "))
    if ans.lower() != "y":
        print(c(C.GRAY, "  취소되었습니다.\n"))
        return
    try:
        reset_practice()
        print(c(C.GREEN, f"\n  ✅ 초기화 완료: {PRACTICE}\n"))
        print(c(C.GRAY, "  생성된 파일:"))
        print(c(C.GRAY, "    logs/access.log"))
        print(c(C.GRAY, "    logs/error_202603.log"))
        print(c(C.GRAY, "    logs/secure.log"))
        print(c(C.GRAY, "    data/docker-compose.yml"))
        print(c(C.GRAY, "    data/user_list.csv"))
        print(c(C.GRAY, "    data/server_info.tsv\n"))
    except Exception as e:
        print(c(C.RED, f"\n  ❌ 초기화 실패: {e}\n"))

def main():
    show_banner()
    print(c(C.GRAY, "  Linux 실습 퀴즈  |  Sangam Beavers  |  Python 3.7+\n"))

    while True:
        divider()
        print(c(C.WHITE, MENU))
        choice = safe_input(c(C.BOLD + C.WHITE, "\n  선택 ▶ "))

        if choice == "exit":
            print(c(C.YELLOW, "\n  👋 수고하셨습니다!\n"))
            break

        elif choice == "1":
            from questions.grep_awk_find import TITLE, QUESTIONS
            from core.engine import run_quiz
            run_quiz(TITLE, QUESTIONS)
            safe_input(c(C.GRAY, "\n  [ Enter ] 메뉴로 돌아가기 ▶ "))
            show_banner()

        elif choice == "2":
            from questions.yaml_json import TITLE, QUESTIONS
            from core.engine import run_quiz
            run_quiz(TITLE, QUESTIONS)
            safe_input(c(C.GRAY, "\n  [ Enter ] 메뉴로 돌아가기 ▶ "))
            show_banner()

        elif choice == "3":
            do_reset()

        else:
            print(c(C.RED, "  ⚠  1, 2, 3 또는 exit 를 입력하세요.\n"))

if __name__ == "__main__":
    main()
