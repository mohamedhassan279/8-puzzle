import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import main
from GUI.solution import StepDisplayWindow


class PuzzleApp(QWidget):

    def __init__(self):
        super().__init__()
        self.flag = False
        self.setWindowTitle("Puzzle Solver")
        self.setGeometry(500, 200, 800, 600)
        self.setFixedSize(800, 600)

        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("QLabel { color: red; font-weight: bold; font-size: 16px}")
        self.error_label.hide()

        self.table_widget = QTableWidget(3, 3)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)

        background_image = QPixmap("GUI/image.jpg")

        widget_width = 800
        widget_height = 600

        # Create a pixmap pattern with the widget's dimensions
        pattern = QPixmap(widget_width, widget_height)
        pattern.fill(Qt.white)
        pattern_painter = QPainter(pattern)
        pattern_painter.drawPixmap(0, 0, background_image)
        pattern_painter.end()

        # Create a brush with the pattern
        background_brush = QBrush(pattern)

        # Create a palette and set the base color to the background brush
        palette = self.table_widget.palette()
        palette.setBrush(QPalette.Base, background_brush)

        # Set the palette for the table
        self.table_widget.setPalette(palette)

        # Increase cell border width using a custom stylesheet
        self.table_widget.setStyleSheet("QTableWidget { border: 2 solid; }")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.table_widget.setFont(font)

        for row in range(3):
            for col in range(3):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.TextWordWrap)
                self.table_widget.setItem(row, col, item)

        self.submit_button1 = self.create_styled_button("BFS")
        self.submit_button2 = self.create_styled_button("DFS")
        self.submit_button3 = self.create_styled_button("A*(Manhattan)")
        self.submit_button4 = self.create_styled_button("A*(Euclidean)")

        self.on_off_button = self.create_off_button("On/Off Steps", checkable=True)
        self.on_off_button.setChecked(True)
        self.on_off_button.clicked.connect(self.toggle_steps)

        self.submit_button1.clicked.connect(self.method1)
        self.submit_button2.clicked.connect(self.method2)
        self.submit_button3.clicked.connect(self.method3)
        self.submit_button4.clicked.connect(self.method4)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button1)
        button_layout.addWidget(self.submit_button2)
        button_layout.addWidget(self.submit_button3)
        button_layout.addWidget(self.submit_button4)

        self.central_layout.addWidget(self.error_label)
        self.central_layout.addWidget(self.table_widget)
        self.central_layout.addLayout(button_layout)
        self.central_layout.addWidget(self.on_off_button)

        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        self.update_row_heights()
        self.resizeEvent = self.custom_resize_event

        # Initialize the step display window
        self.step_display_window = StepDisplayWindow(self)
        self.table_widget.setStyleSheet("""
                    QTableWidget::item {
                        background-color: transparent;
                        color: #754302;
                        border: 1.2 solid #a64f08;
                    }
                    QTableWidget::item:hover {
                        background-color: #d99843;
                    }
                """)

    def create_styled_button(self, text):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                border: none;
                color: white;
                font-size: 15px;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:checked {
                background-color: #e74c3c;
            }
        """)
        return button

    def create_off_button(self, text, checkable=False):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #13bd40;
                border: none;
                color: white;
                font-size: 15px;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #37bf5c;
            }
            QPushButton:checked {
                background-color: #e74c3c;
            }
            QPushButton:checked:hover {
                background-color: #b3404c;
            }
        """)
        if checkable:
            button.setCheckable(True)
        return button

    def custom_resize_event(self, event):
        self.update_row_heights()
        super(PuzzleApp, self).resizeEvent(event)

    def update_row_heights(self):
        height = self.table_widget.height() // self.table_widget.rowCount() - 10
        for row in range(self.table_widget.rowCount()):
            self.table_widget.setRowHeight(row, height)

    def toggle_steps(self):
        self.flag = not self.flag

    def get_flag(self):
        return self.flag

    def solve(self, fun, flag=True, manhattan=True):
        start = self.read_table_input()
        if not main.is_solvable(start):
            self.show_error("Non Solvable")
            return
        else:
            self.hide_error()
        start_time = time.time()
        if flag:
            ans = fun(start)
        else:
            ans = fun(start, manhattan)
        end_time = time.time()
        exec_time = end_time - start_time
        print("Finished in:", round(exec_time * 1e3, 4), "ms")
        if flag:
            trace = main.get_path(ans[0])
        else:
            trace = main.get_path_A(ans[0])
        trace.reverse()
        self.step_display_window.show()
        self.step_display_window.show_steps(self, str(len(trace) - 1), str(ans[1]), str(ans[2]),
                                            str(round(exec_time * 1e3, 5)) + " ms", trace)
        if self.flag:
            print(trace)

    def method1(self):
        if self.validate_input():
            self.solve(main.bfs)

    def method2(self):
        if self.validate_input():
            self.solve(main.dfs)

    def method3(self):
        if self.validate_input():
            self.solve(main.Astar, False)

    def method4(self):
        if self.validate_input():
            self.solve(main.Astar, False, False)

    def read_table_input(self):
        puzzle_input = ""
        blank = False
        values = set()
        for row in range(self.table_widget.rowCount()):
            row_values = ""
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item:
                    value = item.text()
                    if not value:
                        if not blank:
                            blank = True
                            row_values += "0"
                        else:
                            return None
                    elif value.isdigit():
                        value = int(value)
                        if 1 <= value <= 8 and value not in values:
                            values.add(value)
                        else:
                            return None  # Invalid input
                    else:
                        return None
                    row_values += str(value)
            puzzle_input += row_values
        if len(puzzle_input) == 9 and blank:
            return puzzle_input
        return None  # Invalid input

    def validate_input(self):
        puzzle_input = self.read_table_input()
        if puzzle_input is not None:
            return True
        else:
            self.show_error("Invalid input. Make sure values are distinct integers from 1 to 8 with one empty cell.")
            return False

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()

    def hide_error(self):
        self.error_label.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    puzzle_app = PuzzleApp()
    puzzle_app.show()
    sys.exit(app.exec_())
