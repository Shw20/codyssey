import platform
import os
import json
import multiprocessing
import subprocess


class MissionComputer:
    """우주 기지 미션 컴퓨터의 시스템 정보 및 부하 상태를 관리하는 클래스"""

    def __init__(self):
        # 데이터 수집을 위한 저장소 초기화
        self.system_info = {}
        self.load_info = {}

    def get_mission_computer_info(self):
        """[과제] 시스템 사양 정보를 수집하고 JSON 형식으로 출력"""
        try:
            self.system_info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': multiprocessing.cpu_count(),
                'memory_size': self._get_total_memory() # OS별 상세 조회를 위한 내부 호출
            }

            filtered_info = self._filter_by_settings(self.system_info)
            
            print('--- Mission Computer System Info ---')
            print(json.dumps(filtered_info, indent=4))
            return filtered_info

        except Exception as e:
            print(f'시스템 정보 획득 중 오류: {e}')
            return None

    def get_mission_computer_load(self):
        """[과제] 실시간 부하(CPU/메모리)를 측정하고 JSON 형식으로 출력"""
        try:
            self.load_info = {
                'cpu_realtime_usage': self._get_cpu_usage(),
                'memory_realtime_usage': self._get_memory_usage()
            }

            filtered_load = self._filter_by_settings(self.load_info)
            
            print('--- Mission Computer Real-time Load ---')
            print(json.dumps(filtered_load, indent=4))
            return filtered_load

        except Exception as e:
            print(f'부하 정보 획득 중 오류: {e}')
            return None

    def _get_total_memory(self):
        """[메모] Windows PowerShell 또는 Linux procfs를 통해 전체 메모리 용량 계산"""
        try:
            if platform.system() == 'Windows':
                # wmic 미지원 대응: PowerShell 명령어로 실제 물리 메모리 합계 계산
                cmd = ['powershell', '-Command', '(Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum).Sum']
                output = subprocess.check_output(cmd).decode().strip()
                return f"{int(output) / (1024**3):.2f} GB"
            else:
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if 'MemTotal' in line:
                            return f"{int(line.split()[1]) / 1024 / 1024:.2f} GB"
        except:
            return 'Unknown'

    def _get_cpu_usage(self):
        """[메모] 실시간 CPU 사용률 획득 (Windows/Linux 분기 처리)"""
        try:
            if platform.system() == 'Windows':
                # PowerShell로 프로세서 로드율(%) 직접 조회
                cmd = ['powershell', '-Command', '(Get-CimInstance Win32_Processor).LoadPercentage']
                output = subprocess.check_output(cmd).decode().strip()
                return f"{output}%"
            elif hasattr(os, 'getloadavg'):
                load = os.getloadavg()[0]
                return f"{(load / multiprocessing.cpu_count()) * 100:.2f}%"
            return 'N/A'
        except:
            return 'N/A'

    def _get_memory_usage(self):
        """[메모] 가용 메모리 대비 사용량 비율 계산"""
        try:
            if platform.system() == 'Windows':
                # 전체 메모리와 사용 가능한 메모리 차이를 이용해 백분율 산출
                cmd_total = ['powershell', '-Command', '(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory']
                cmd_free = ['powershell', '-Command', '(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory']
                
                total = int(subprocess.check_output(cmd_total).decode().strip())
                free = int(subprocess.check_output(cmd_free).decode().strip()) * 1024
                
                used_pct = ((total - free) / total) * 100
                return f"{used_pct:.1f}%"
            else:
                with open('/proc/meminfo', 'r') as f:
                    mem = {l.split(':')[0]: int(l.split()[1]) for l in f}
                used = mem['MemTotal'] - mem.get('MemFree', 0) - mem.get('Buffers', 0) - mem.get('Cached', 0)
                return f"{(used / mem['MemTotal']) * 100:.1f}%"
        except:
            return 'N/A'

    def _filter_by_settings(self, data_dict):
        """[보너스] setting.txt에 명시된 항목만 필터링하여 반환"""
        if not os.path.exists('setting.txt'):
            return data_dict
        try:
            with open('setting.txt', 'r', encoding='utf-8') as f:
                keys = [line.strip() for line in f if line.strip()]
            return {k: v for k, v in data_dict.items() if k in keys} if keys else data_dict
        except:
            return data_dict


if __name__ == '__main__':
    # 클래스 인스턴스화 (runComputer) 및 실행
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()

    # 실행결과 윈도우 환경으로 인해 값을 제대로 불러오지 못한다는 문제가 있음