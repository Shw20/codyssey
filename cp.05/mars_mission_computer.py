# 더미 센서 클래스 구현
import random

# DummySensor라는 센서 기계 설계도(클래스)를 만듬 (캡슐화)
class DummySensor:
    """
    화성 기지의 환경 데이터를 무작위로 생성하는 가상 센서 클래스입니다.
    """

    # __init__ 은 생성자, 객체 생성 시 초기상태를 설정
    def __init__(self):
        # self.env_values는 클래스 내부에서 사용하는 변수(멤버)
        # 파이썬의 Dictionary 형식 사용해 각 환경 데이터를 key value로 관리 (JSON과 유사)
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    # 환경 데이터를 무작위로 설정하는 메서드
    def set_env(self):
        """
        각 환경 항목에 대해 지정된 범위 내의 랜덤 값을 생성하여 저장합니다.
        """
        # random.randint(A, B)는 A와 B사이의 정수를 랜덤으로 뽑아줌

        # 내부 온도 (18~30도)
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        
        # 외부 온도 (0~21도)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        
        # 내부 습도 (50~60%)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        
        # 외부 광량 (500~715 W/m2)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        
        # 내부 이산화탄소 농도 (0.02~0.1%)
        # 정수만 나오는 randint, 2~10 뽑고 100으로 나눠 소수점 수치 맞춤
        self.env_values['mars_base_internal_co2'] = random.randint(2, 10) / 100
        
        # 내부 산소 농도 (4%~7%)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)

    # 저장된 환경 데이터를 가져오는 메서드
    def get_env(self):
        # 가공된 데이터(사전객체) 를 외부로 반환
        return self.env_values


# --- 메인 실행 ---
if __name__ == '__main__':
    # 1. DummySensor 클래스를 ds라는 이름의 인스턴스로 생성
    # 설계도(class)를 바탕으로 실제 물건(instance)인 ds 호출
    ds = DummySensor()
    
    # 2. set_env() 호출해 랜덤값을 뽑는 함수 호출
    ds.set_env()
    
    # 3. get_env() 호출해 측정값을 가져와 변수에 담기
    current_env = ds.get_env()
    
    # 4. 결과 출력 
    print('--- 화성 기지 환경 모니터링 데이터 ---')
    # items()를 사용하면 사전에 key value를 동시에 꺼내 반복문을 돌릴 수 있음.
    for key, value in current_env.items():
        # 항목 이름과 값을 보기 좋게 출력
        print(f'{key}: {value}')
    print('------------------------------------')