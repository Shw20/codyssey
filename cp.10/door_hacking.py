import zipfile
import time
import itertools
import zlib


def unlock_zip_smart():
    '''CPU 부하를 최소화하면서 지능적으로 암호를 탐색'''
    zip_file_path = r'c:/school/DMU/codyssey/cp.10/emergency_storage_key.zip'
    output_file = r'c:/school/DMU/codyssey/cp.10/password.txt'
    
    # 전략적 순서 배치: 사람들이 자주 쓰는 소문자 알파벳을 숫자보다 앞에 배치
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    password_length = 6
    
    try:
        with zipfile.ZipFile(zip_file_path) as z_file:
            start_time = time.time()
            print(f'저부하 지능형 해킹 시작: {time.ctime(start_time)}')
            print('접근 중...')
            
            count = 0
            for combo in itertools.product(chars, repeat=password_length):
                password = ''.join(combo)
                count += 1
                
                try:
                    z_file.setpassword(password.encode('utf-8'))
                    if z_file.testzip() is None:
                        # 성공 시 로직
                        print(f'\n🎉 암호 발견: {password}')
                        with open(output_file, 'w') as f:
                            f.write(password)
                        return password
                
                except (RuntimeError, zipfile.BadZipFile, zlib.error):
                    # 1,000번 시도할 때마다 0.01초씩 쉬어줍니다 (CPU 과열 방지)
                    if count % 1000 == 0:
                        time.sleep(0.001) 
                    
                    if count % 100000 == 0:
                        elapsed = time.time() - start_time
                        print(f'가동 중... {count:,}회 시도 ({elapsed:.1f}초)')
                    continue

    except Exception as e:
        print(f'오류 발생: {e}')


if __name__ == '__main__':
    unlock_zip_smart()