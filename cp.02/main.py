def file_log(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8')as f:
            lines = f.readlines()
        errors = [line.strip() for line in lines if "ERROR" in line]
        return errors
    except FileNotFoundError:
        return "파일을 찾을 수 없습니다."

def save_report(errors):
    with open("report.md", "w", encoding="utf-8") as f:
        f.write("# 파악된 사고 원인\n")
        if isinstance(errors, list) and errors:
            for err in errors:
                f.write(f"- {err}\n")
        else:
            f.write("문제 없음\n")
    print("보고서가 생성되었습니다")
    
# --- 실행부 ---
# 테스트를 위해 임시 로그 파일 생성
with open("logs.txt", "w", encoding="utf-8") as f:
    f.write("System Start\nERROR: CPU Fan Failure\nERROR: Memory Overload\nSystem End")

# 로그 분석 후 마크다운 저장
found_errors = file_log("logs.txt")
save_report(found_errors)

# 