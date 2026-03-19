import sys

class C:
    RESET   = "\033[0m";  BOLD    = "\033[1m"
    RED     = "\033[91m"; GREEN   = "\033[92m"
    YELLOW  = "\033[93m"; CYAN    = "\033[96m"
    WHITE   = "\033[97m"; GRAY    = "\033[90m"
    MAGENTA = "\033[95m"; BLUE    = "\033[94m"
    BG_BLUE  = "\033[44m"; BG_GREEN = "\033[42m"
    BG_RED   = "\033[41m"; BG_GRAY  = "\033[100m"
    BG_MAG   = "\033[45m"

def c(color, text): return f"{color}{text}{C.RESET}"
def divider(ch="─", w=62, col=C.GRAY): print(c(col, ch * w))

def safe_input(prompt=""):
    try:    return input(prompt).strip()
    except: return "exit"

def show_code(code):
    print(c(C.GRAY, "  ┌" + "─"*54 + "┐"))
    for line in code.splitlines():
        padded = line[:54].ljust(54)
        print(c(C.YELLOW, f"  │ {padded} │"))
    print(c(C.GRAY, "  └" + "─"*54 + "┘"))

def show_context(ctx):
    print(c(C.BLUE, "  ┌─ 배경 " + "─"*50 + "┐"))
    for line in ctx.strip().splitlines():
        padded = line[:56].ljust(56)
        print(c(C.BLUE, "  │ ") + c(C.WHITE, padded) + c(C.BLUE, "│"))
    print(c(C.BLUE, "  └" + "─"*58 + "┘"))
    print()

def grade_short(user_ans, q):
    acceptable = q.get("acceptable", [q.get("answer", "")])
    match_type = q.get("match_type", "exact")
    case_sens  = q.get("case_sensitive", False)
    ua = user_ans if case_sens else user_ans.lower().strip()
    for acc in acceptable:
        if isinstance(acc, list):
            # multi: all keywords must appear
            if all(x.lower() in ua for x in acc):
                return True
        else:
            a = str(acc) if case_sens else str(acc).lower().strip()
            if match_type == "exact"      and ua == a:           return True
            if match_type == "contains"   and a in ua:           return True
            if match_type == "startswith" and ua.startswith(a):  return True
    return False

def ask_mcq(q):
    for opt in q["options"]:
        print(f"  {opt}")
    print()
    while True:
        ans = safe_input(c(C.WHITE, "  번호 입력 (1~4) ▶ "))
        if ans == "exit": return None
        if ans in ("1","2","3","4"): return int(ans)
        print(c(C.RED, "  ⚠  1~4 중 하나를 입력하세요."))

def ask_short(q):
    if q.get("hint"):
        print(c(C.GRAY, f"  💭 힌트: {q['hint']}"))
    print()
    ans = safe_input(c(C.WHITE, "  명령어 입력 ▶ "))
    if ans == "exit": return None
    return ans

def show_result(ok, q, user_ans, is_mcq):
    correct_disp = (str(q["answer"]) + "번") if is_mcq else f'"{q["answer"]}"'
    if ok:
        print(c(C.GREEN, "\n  ✅ 정답!\n"))
    else:
        print(c(C.RED, "\n  ❌ 오답!"))
        if not is_mcq:
            print(c(C.RED, f"     입력값:  {user_ans}"))
        print(c(C.GREEN, f"     정답:    {correct_disp}\n"))
    print(c(C.GRAY, "  💡 해설: ") + q["explain"])
    if q.get("tip"):
        print(c(C.YELLOW, "  🔖 암기: ") + q["tip"])
    print()

def _handle_one(sub, label):
    """단일 문제 처리. (is_correct, exit_flag) 반환"""
    qtype = sub.get("type", "short")
    badge = (c(C.BG_BLUE + C.WHITE, " 객관식 ") if qtype == "mcq"
             else c(C.BG_GRAY + C.WHITE, " 주관식 "))
    print(f"  {badge}  {c(C.BOLD + C.CYAN, label + '. ' + sub['q'])}")
    if sub.get("practice_file"):
        print(c(C.MAGENTA, "  📂 파일: ") + c(C.WHITE, sub["practice_file"]))
    if sub.get("code"):
        print()
        show_code(sub["code"])
    print()

    if qtype == "mcq":
        user_ans = ask_mcq(sub)
        if user_ans is None: return False, True
        ok = (user_ans == sub["answer"])
        show_result(ok, sub, user_ans, True)
        return ok, False
    else:
        user_ans = ask_short(sub)
        if user_ans is None: return False, True
        ok = grade_short(user_ans, sub)
        show_result(ok, sub, user_ans, False)
        return ok, False

def run_quiz(title, questions):
    """퀴즈 실행. exit 시 메뉴로 복귀. (score, total) 반환"""
    score = 0
    records = []   # (label, q_text, type, correct)

    print()
    print(c(C.BG_MAG + C.BOLD + C.WHITE, f"  📚 {title}  "))
    print(c(C.GRAY, "  'exit' 입력 시 메뉴로 복귀\n"))

    q_idx = 0
    for qi, q in enumerate(questions):
        q_idx += 1
        qtype = q.get("type", "short")
        divider()

        if qtype == "group":
            # ── 그룹 문제 ──────────────────────────────
            print(c(C.BOLD + C.WHITE, f"  Q{q['num']}. {q['title']}"))
            print()
            if q.get("context"):
                show_context(q["context"])

            subs = q["subquestions"]
            for si, sub in enumerate(subs):
                label = f"Q{q['num']}-{si+1}"
                ok, exited = _handle_one(sub, label)
                score += int(ok)
                records.append((label, sub["q"][:44], sub.get("type","short"), ok))
                if exited:
                    _exit_notice(score, records)
                    return score, len(records)
                if si < len(subs) - 1:
                    safe_input(c(C.GRAY, "  [ Enter ] 다음 소문제 ▶ "))
        else:
            # ── 단일 문제 ──────────────────────────────
            label = f"Q{q.get('num', q_idx)}"
            ok, exited = _handle_one(q, label)
            score += int(ok)
            records.append((label, q["q"][:44], qtype, ok))
            if exited:
                _exit_notice(score, records)
                return score, len(records)

        if qi < len(questions) - 1:
            safe_input(c(C.GRAY, "  [ Enter ] 다음 문제 ▶ "))

    show_score(score, records)
    return score, len(records)

def _exit_notice(score, records):
    print(c(C.YELLOW, "\n  ↩  메뉴로 돌아갑니다.\n"))
    show_score(score, records)

def show_score(score, records):
    total = len(records)
    if total == 0: return
    pct = score / total * 100
    divider("═", col=C.CYAN)

    if pct == 100:  badge = c(C.BG_GREEN + C.BOLD, " 🏆 PERFECT ")
    elif pct >= 80: badge = c(C.BG_GREEN + C.BOLD, " ✨ PASS    ")
    elif pct >= 60: badge = c(C.BG_BLUE  + C.BOLD, " 📖 KEEP GOING ")
    else:           badge = c(C.BG_RED   + C.BOLD, " 💪 MORE PRACTICE ")

    print(f"\n  {badge}  {c(C.BOLD+C.WHITE, f'{score}/{total}문제  ({pct:.0f}%)')}\n")

    wrongs = [(l, q, t) for l, q, t, ok in records if not ok]
    if wrongs:
        print(c(C.RED + C.BOLD, "  ── 틀린 문제 ─────────────────────────────────"))
        for l, q, t in wrongs:
            tag = "[객관식]" if t == "mcq" else "[주관식]"
            print(c(C.RED, f"  {l} {tag}  {q}..."))
        print()
    divider("═", col=C.CYAN)
