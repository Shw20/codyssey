import time
import json
import random


class DummySensor:
    """기존 문제 3에서 정의된 가상의 센서 데이터를 생성하는 클래스"""

    def get_temperature(self):
        # 지정된 범위 내에서 float값 생성
        return round(random.uniform(-100.0, 30.0), 2)

    def get_humidity(self):
        return round(random.uniform(0.0, 100.0), 2)

    def get_illuminance(self):
        return round(random.uniform(0.0, 20000.0), 2)

    def get_gas_level(self):
        # 이산화탄소와 산소 농도 시뮬레이션용
        return round(random.uniform(0.0, 100.0), 2)


class MissionComputer:
    """화성 기지의 환경 데이터를 수집하고 출력하는 미션 컴퓨터 클래스"""

    def __init__(self):
        # 환경 정보를 저장할 딕셔너리 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        # 센서 인스턴스 생성
        self.ds = DummySensor()
        # 매 5초마다의 데이터를 저장, 평균 계산을 위한 데이터 누적 리스트
        self.history = []

    def get_sensor_data(self):
        """
        센서 데이터를 가져와 업데이트하고 JSON 형식으로 출력.
        5초 주기 반복 및 5분 평균 산출 기능 포함.
        """
        print('Mission Computer 모니터링이 시작되었습니다...')
        print('Ctrl+C 입력시 실행 중단합니다.')

        last_avg_time = time.time()

        try:
            while True:
                # 1. 센서 인스턴스로부터 최신 값 fetch 후 state 업데이트
                self.env_values['mars_base_internal_temperature'] = self.ds.get_temperature()
                self.env_values['mars_base_external_temperature'] = self.ds.get_temperature()
                self.env_values['mars_base_internal_humidity'] = self.ds.get_humidity()
                self.env_values['mars_base_external_illuminance'] = self.ds.get_illuminance()
                self.env_values['mars_base_internal_co2'] = self.ds.get_gas_level()
                self.env_values['mars_base_internal_oxygen'] = self.ds.get_gas_level()

                # 2. Dictionary를 JSON 문자열로 변환하여 CLI에 출력
                json_output = json.dumps(self.env_values, indent=4)
                print(f'\n--- Current Environment Data ---\n{json_output}')

                # 3. 평균 계산을 위해 현재 상태의 Snapshot을 리스트에 복사하여 저장
                # .copy()를 쓰는 이유는 참조가 아닌 값 자체를 저장하기 위함 (Deep Copy와 유사)
                self.history.append(self.env_values.copy())

                # ***보너스***
                #  5분(300초)마다 평균값 계산 및 출력
                current_time = time.time()
                if current_time - last_avg_time >= 300: 
                    self._display_average_data() # 평균값 산출 메서드 호출
                    last_avg_time = current_time # 타이머 리셋
                    self.history = []  # 평균 출력 후 메모리 관리상 이력 초기화

                # 5초간 일시 정지
                time.sleep(5)

        # ***보너스***
        except KeyboardInterrupt:
            # 특정 키(Ctrl+C) 입력 시 종료
            print('\nSystem stopped....')

    def _display_average_data(self):
        """5분간 축적된 데이터의 평균을 계산하여 출력"""
        if not self.history:
            return

        print('\n' + '=' * 40)
        print('*** 5-Minute Average Report ***')
        keys = self.env_values.keys()
        avg_report = {}

        # 각 키별 평균 계산
        for key in keys:
            # List Comprehension을 사용하여 특정 항목의 총합 계산
            total = sum(data[key] for data in self.history)
            avg_report[key] = round(total / len(self.history), 2)

        # 최종 통계 JSON 출력
        print(json.dumps(avg_report, indent=4))
        print('=' * 40)


if __name__ == '__main__':
    # Entry Point: 어플리케이션 실행
    # MissionComputer 인스턴스화
    RunComputer = MissionComputer()
    # 센서 데이터 수집 시작
    RunComputer.get_sensor_data()