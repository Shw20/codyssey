# 로그 읽고 분석하는 함수
def file_log(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8')as f:
            lines = f.readlines()
        errors = [line.strip() for line in lines if "ERROR" in line]
        return errors
    # 파일이 없으면 메세지 출력
    except FileNotFoundError:
        return "파일을 찾을 수 없습니다."

# 파일 작성 함수
def save_report(errors):
    # 파일 열기(with : 읽거나 쓰고난 뒤 파일을 닫아줌), 한글 깨짐 방지 위해 utf-8 인코딩
    with open("report.md", "w", encoding="utf-8") as f:
        f.write("에러\n")
        # 로그에서 err 키워드 포함시 골라냄
        if isinstance(errors, list) and errors:
            for err in errors:
                f.write(f"- {err}\n")
        else:
            f.write("문제 없음\n")
    print("파일 생성됨")

# 임시 로그 파일 생성
with open("logs.txt", "w", encoding="utf-8") as f:
    f.write("System Start\nERROR: CPU Fan Failure\nERROR: Memory Overload\nSystem End")

# 마크다운 저장
found_errors = file_log("logs.txt")
save_report(found_errors)
print("Hello Mars")

