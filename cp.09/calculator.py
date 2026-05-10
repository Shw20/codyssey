import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Calculator:
    '''계산기의 핵심 연산 로직을 담당하는 클래스'''

    def __init__(self):
        self.reset()

    def reset(self):
        '''모든 값을 초기화'''
        self.current_value = '0'
        self.stored_value = 0
        self.pending_operation = None
        self.is_ready_for_new_number = True

    def add_digit(self, digit):
        '''숫자 입력 및 누적'''
        if self.is_ready_for_new_number:
            self.current_value = str(digit)
            self.is_ready_for_new_number = False
        else:
            if self.current_value == '0':
                self.current_value = str(digit)
            else:
                self.current_value += str(digit)
        return self.current_value

    def add_decimal(self):
        '''소수점 입력 (중복 방지)'''
        if self.is_ready_for_new_number:
            self.current_value = '0.'
            self.is_ready_for_new_number = False
        elif '.' not in self.current_value:
            self.current_value += '.'
        return self.current_value

    def toggle_sign(self):
        '''양수/음수 전환'''
        if self.current_value.startswith('-'):
            self.current_value = self.current_value[1:]
        elif self.current_value != '0':
            self.current_value = '-' + self.current_value
        return self.current_value

    def apply_percent(self):
        '''백분율 계산'''
        try:
            val = float(self.current_value) / 100
            self.current_value = self._format_number(val)
            return self.current_value
        except ValueError:
            return 'Error'

    def set_operation(self, operation):
        '''연산자 설정'''
        try:
            val = float(self.current_value)
            if self.pending_operation:
                self.equal()
                val = float(self.current_value)
            
            self.stored_value = val
            self.pending_operation = operation
            self.is_ready_for_new_number = True
        except ValueError:
            self.reset()

    def equal(self):
        '''계산 실행'''
        if not self.pending_operation:
            return self.current_value

        try:
            current = float(self.current_value)
            if self.pending_operation == '+':
                result = self.stored_value + current
            elif self.pending_operation == '-':
                result = self.stored_value - current
            elif self.pending_operation == '*':
                result = self.stored_value * current
            elif self.pending_operation == '/':
                if current == 0:
                    return 'Error'
                result = self.stored_value / current
            
            self.current_value = self._format_number(result)
            self.pending_operation = None
            self.is_ready_for_new_number = True
            return self.current_value
        except (ValueError, OverflowError):
            self.reset()
            return 'Error'

    def _format_number(self, value):
        '''숫자 포맷팅 (반올림 및 정수 처리)'''
        # 소수점 6자리 반올림
        value = round(value, 6)
        if value == int(value):
            return str(int(value))
        return str(value)


class CalculatorApp(QWidget):
    '''UI 생성 및 Calculator 클래스와 연결'''

    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Han\'s Calculator')
        self.setFixedSize(300, 450)
        self.setStyleSheet('background-color: #000000;')

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # 디스플레이 설정
        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet('color: white; padding: 10px;')
        self.update_font_size()
        layout.addWidget(self.display)

        # 버튼 그리드 설정
        grid = QGridLayout()
        buttons = [
            ('AC', 0, 0), ('+/-', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        for btn_text, *pos in buttons:
            button = QPushButton(btn_text)
            button.setFixedSize(60 if len(pos) < 4 else 130, 60)
            button.clicked.connect(self.on_click)
            
            # 스타일 입히기
            if btn_text in ['/', '*', '-', '+', '=']:
                color = 'background-color: #FF9F0A; color: white;'
            elif btn_text in ['AC', '+/-', '%']:
                color = 'background-color: #A5A5A5; color: black;'
            else:
                color = 'background-color: #333333; color: white;'
            
            button.setStyleSheet(f'border-radius: 30px; font-size: 18pt; {color}')
            grid.addWidget(button, *pos)

        layout.addLayout(grid)
        self.setLayout(layout)

    def update_font_size(self):
        '''출력 값의 길이에 따라 폰트 크기 자동 조정 (보너스 과제)'''
        text_length = len(self.display.text())
        if text_length <= 7:
            font_size = 40
        elif text_length <= 11:
            font_size = 30
        else:
            font_size = 20
        self.display.setFont(QFont('Arial', font_size))

    def on_click(self):
        sender = self.sender().text()

        if sender.isdigit():
            res = self.calc.add_digit(sender)
        elif sender == '.':
            res = self.calc.add_decimal()
        elif sender == 'AC':
            self.calc.reset()
            res = '0'
        elif sender == '+/-':
            res = self.calc.toggle_sign()
        elif sender == '%':
            res = self.calc.apply_percent()
        elif sender in ['+', '-', '*', '/']:
            self.calc.set_operation(sender)
            res = self.calc.current_value
        elif sender == '=':
            res = self.calc.equal()

        self.display.setText(res)
        self.update_font_size()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalculatorApp()
    ex.show()
    sys.exit(app.exec_())