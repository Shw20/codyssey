import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_value = ''  # 현재 입력된 숫자
        self.first_value = None  # 첫 번째 피연산자
        self.operator = None     # 선택된 연산자
        self.restart_flag = False # 계산 후 새로 시작할지 여부

    def init_ui(self):
        # 메인 레이아웃 (수직 배치)
        main_layout = QVBoxLayout()
        
        # 1. 숫자창 (Display) 설정
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)  # 직접 타이핑 금지
        self.display.setAlignment(Qt.AlignRight)  # 오른쪽 정렬
        self.display.setStyleSheet('font-size: 40px; padding: 10px; border: none;')
        main_layout.addWidget(self.display)

        # 2. 버튼 레이아웃 (그리드 배치)
        grid = QGridLayout()
        
        # 버튼 배치 (아이폰 스타일 배열)
        buttons = [
            ('C', 0, 0), ('+/-', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        # 버튼 생성 및 레이아웃 추가
        for btn_text in buttons:
            text = btn_text[0]
            row = btn_text[1]
            col = btn_text[2]
            
            # 0 버튼처럼 칸을 합쳐야 하는 경우 처리
            if len(btn_text) == 5:
                row_span = btn_text[3]
                col_span = btn_text[4]
                button = QPushButton(text)
                grid.addWidget(button, row, col, row_span, col_span)
            else:
                button = QPushButton(text)
                grid.addWidget(button, row, col)
            
            button.setFixedSize(60, 60) if text != '0' else button.setFixedSize(125, 60)
            button.clicked.connect(self.on_click) # 이벤트 연결

        main_layout.addLayout(grid)
        self.setLayout(main_layout)
        self.setWindowTitle('Mars Calculator')
        self.show()

    def on_click(self):
        btn = self.sender()
        key = btn.text()

        if key in '0123456789.':
            if self.restart_flag:
                self.current_value = key
                self.restart_flag = False
            else:
                self.current_value += key
            self.display.setText(self.current_value)

        elif key == 'C':
            self.current_value = ''
            self.first_value = None
            self.operator = None
            self.display.setText('0')

        elif key in '+-*/':
            self.first_value = float(self.display.text())
            self.operator = key
            self.current_value = ''

        elif key == '=':
            if self.operator and self.current_value:
                second_value = float(self.current_value)
                if self.operator == '+': result = self.first_value + second_value
                elif self.operator == '-': result = self.first_value - second_value
                elif self.operator == '*': result = self.first_value * second_value
                elif self.operator == '/': 
                    result = self.first_value / second_value if second_value != 0 else 'Error'
                
                self.display.setText(str(result))
                self.restart_flag = True
                self.current_value = str(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculator()
    sys.exit(app.exec_())