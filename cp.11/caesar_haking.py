import sys


def caesar_cipher_decode(target_text):
    '''카이사르 암호의 모든 경우의 수를 계산하고 출력하는 함수'''
    # 알파벳 총 개수 (26개)
    alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    results = {}

    print(f'해독 대상 문자열: {target_text}')
    print('-' * 40)

    # 0부터 25까지 모든 자리수(Shift) 시도
    for shift in range(26):
        decoded_text = ''
        for char in target_text:
            if char in alphabet_lower:
                idx = (alphabet_lower.find(char) - shift) % 26
                decoded_text += alphabet_lower[idx]
            elif char in alphabet_upper:
                idx = (alphabet_upper.find(char) - shift) % 26
                decoded_text += alphabet_upper[idx]
            else:
                # 공백이나 특수문자는 그대로 유지
                decoded_text += char
        
        results[shift] = decoded_text
        print(f'Shift {shift:2}: {decoded_text}')

        # 보너스 과제: 간단한 사전 검사 (영문 핵심 단어 포함 여부)
        # 화성 기지에서 쓸법한 단어들을 사전으로 정의
        dictionary = ['open', 'door', 'access', 'password', 'key', 'secret', 'mars']
        for word in dictionary:
            if word in decoded_text.lower():
                print(f'>> [알림] 단어 "{word}" 발견! 유력한 암호 후보입니다.')

    print('-' * 40)
    return results


def main():
    input_file = 'password.txt'
    output_file = 'result.txt'
    
    try:
        # 1. password.txt 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            target_text = f.read().strip()
        
        if not target_text:
            print('파일 내용이 비어 있습니다.')
            return

        # 2. 암호 해독 실행 (모든 결과 출력)
        decoded_results = caesar_cipher_decode(target_text)

        # 3. 사용자로부터 해독된 번호 입력 받기
        try:
            choice = input('해독에 성공한 Shift 번호를 입력하세요 (취소: Enter): ')
            if choice.isdigit() and int(choice) in decoded_results:
                final_password = decoded_results[int(choice)]
                
                # 4. 결과 저장
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(final_password)
                print(f'최종 암호가 "{output_file}"에 저장되었습니다: {final_password}')
            else:
                print('올바른 번호가 입력되지 않아 저장하지 않고 종료합니다.')
        except EOFError:
            pass

    except FileNotFoundError:
        print(f'에러: {input_file} 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'예상치 못한 시스템 오류 발생: {e}')


if __name__ == '__main__':
    main()