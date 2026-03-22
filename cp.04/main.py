# 화성 기지의 수많은 자재 중 어떤 것이 가장 먼저 폭팔할 위험이 있는지
# 인화성 지수 0.7을 기준으로 파악
# 다른 시스템에서 빠르게 불러올 수 있게 이진파일로도 보관

def process_mars_inventory():
    # 파일명 정의
    file_path = 'Mars_Base_Inventory_List.csv'
    danger_file_path = 'Mars_Base_Inventory_danger.csv' # 인화성 0.7 이상
    binary_file_path = 'Mars_Base_Inventory_List.bin' # 인화성 순 전체목록(이진파일)
    # 메모장으로 열면 글자가 깨져보이지만, 프로그램으로 빠르게 읽을 수 있음.
    
    inventory_list = [] # 파일 내용
    header = '' # 파일 맨 윗줄 변수

    # 1 & 2. 파일 읽기 및 리스트 변환
    try:
        f = open(file_path, 'r', encoding='utf-8') # 읽기포드로 열고 urf-8 인코딩
        content = f.read().splitlines() # 한줄한줄 읽어 list로 만듬
        f.close() # 파일 닫기

        if not content:
            return # 내용 없으면 return

        header = content[0]  # 첫 줄 따로 보관

        # 두 번째 줄부터 끝까지 하나씩 꺼냄
        for line in content[1:]: 
            row = line.split(',') # (,)로 잘라 데이터 가공
            if len(row) < 5:      # 데이터 없으면 건너뜀
                continue
            
            # 인화성 지수를 숫자로 바꿈(float)
            try:
                row[4] = float(row[4])
            except ValueError:
                row[4] = 0.0 # 숫자로 못 바꾸면 0으로
            
            inventory_list.append(row) # 가공된 데이터 넣기
                
        print('데이터 로드 완료\n')

    except FileNotFoundError:
        print('에러: 파일을 찾을 수 없습니다.')
        return
    except Exception as e:
        print(f'오류 발생: {e}')
        return

    # 3. 인화성이 높은 순(내림차순)으로 정렬
    # 인화성 지수 비교해 큰 값을 위로 올림
    for i in range(len(inventory_list)):
        for j in range(i + 1, len(inventory_list)):
            # 앞보다 뒤가 크면 자리 바꾸기
            if inventory_list[i][4] < inventory_list[j][4]:
                inventory_list[i], inventory_list[j] = inventory_list[j], inventory_list[i]

    # 4. 인화성 지수 0.7 이상 목록 출력
    print('--- 인화성 위험 물질 목록 (0.7 이상) ---')
    danger_list = [] # 0.7이상만 담을 배열
    for item in inventory_list:
        if item[4] >= 0.7: # 0.7 이상인 것만
            danger_list.append(item)
            print(f"물질: {item[0]}, 지수: {item[4]}")
    print('---------------------------------------\n')

    # 5. 위험 목록을 CSV 포멧으로 저장 (기본 write 사용)
    try:
        f_out = open(danger_file_path, 'w', encoding='utf-8') # 쓰기모드
        f_out.write(header + '\n') # 맨 위에 제목 먼저
        for item in danger_list:
            # 리스트 요소를 다시 쉼표로 문자열로 합치기
            line = ','.join([str(val) for val in item])
            f_out.write(line + '\n')
        f_out.close()
        print(f'{danger_file_path} 저장 완료')
    except Exception as e:
        print(f'CSV 저장 에러: {e}')

    # 보너스 과제 1. 이진 파일 형태로 저장 (pickle 없이 저장)
    # 문자열을 바이트로 변환
    try:
        f_bin = open(binary_file_path, 'wb') # 바이트 쓰기모드
        for item in inventory_list:
            line = ','.join([str(val) for val in item]) + '\n'
            f_bin.write(line.encode('utf-8'))# 문자열을 바이트로 인코딩
        f_bin.close()
        print(f'{binary_file_path} 저장 완료')
    except Exception as e:
        print(f'이진 파일 저장 에러: {e}')

    # 보너스 과제 2. 이진 파일 읽기 및 출력
    try:
        print('\n--- 이진 파일 내용 읽기 ---')
        f_bin_in = open(binary_file_path, 'rb') # 바이트 읽기모드
        binary_data = f_bin_in.read().decode('utf-8') # 문자로 다시 해석
        f_bin_in.close()
        print(binary_data[:200] + '...') # 데이터 일부만 출력
    except Exception as e:
        print(f'이진 파일 읽기 에러: {e}')

# 직접 실행될 때만 함수 실행
if __name__ == '__main__':
    process_mars_inventory()