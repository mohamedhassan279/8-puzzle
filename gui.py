import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import main



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
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)

        background_image = QPixmap("wooden.jpg")

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
        self.table_widget.setStyleSheet("QTableWidget::item { border: 1px solid brown; }")
        font = QFont()
        font.setPointSize(20)  # Adjust the font size as needed
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
                        color: #000000; /* Set the text color to black */
                        font: 16px;
                        text-align: center
                    }
                    QTableWidget::item:hover {
                        background-color: #e39271;
                    }
                """)

    def custom_resize_event(self, event):
        self.update_row_heights()
        super(PuzzleApp, self).resizeEvent(event)

    def update_row_heights(self):
        height = self.table_widget.height() // self.table_widget.rowCount() - 16
        for row in range(self.table_widget.rowCount()):
            self.table_widget.setRowHeight(row, height)

    def toggle_steps(self):
        self.flag = not self.flag

    def get_flag(self):
        return self.flag

    def solve(self, fun, flag=True, manhattan=True):
        print("hi")
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
        print(ans)
        end_time = time.time()
        exec_time = end_time - start_time
        print("Finished in:", round(exec_time * 1e3, 4), "ms")
        if flag:
            trace = main.get_path(ans[0])
        else:
            trace = main.get_path_A(ans[0])
        trace.reverse()
        self.step_display_window.show()
        self.step_display_window.show_steps(self, str(len(trace)-1), str(ans[1]), str(ans[2]), str(round(exec_time * 1e3, 5)) + " ms", trace)
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
        values = set()
        for row in range(self.table_widget.rowCount()):
            row_values = ""
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item:
                    value = item.text()
                    if not value:
                        value = "0"
                    value = int(value)
                    if 0 <= value <= 8 and value not in values:
                        values.add(value)
                    else:
                        return None  # Invalid input
                    row_values += str(value)
            puzzle_input += row_values
        if len(values) == 9:
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

    def create_styled_button(self, text, checkable=False):
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
        if checkable:
            button.setCheckable(True)
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


class StepDisplayWindow(QWidget):
    def __init__(self, win):
        super().__init__()
        self.wn = win
        self.setWindowTitle("Step Display")
        self.setGeometry(100, 100, 400, 300)

        self.label1 = QLabel()
        self.label1.setStyleSheet("QLabel { color: red; font-weight: bold; font-size: 16px}")
        self.label1.hide()
        self.label2 = QLabel()
        self.label2.setStyleSheet("QLabel { color: red; font-weight: bold; font-size: 16px}")
        self.label2.hide()
        self.label3 = QLabel()
        self.label3.setStyleSheet("QLabel { color: red; font-weight: bold; font-size: 16px}")
        self.label3.hide()
        self.label4 = QLabel()
        self.label4.setStyleSheet("QLabel { color: red; font-weight: bold; font-size: 16px}")
        self.label4.hide()

        # if PuzzleApp.flag:
        self.step_table = QTableWidget(3, 3)
        self.step_table.verticalHeader().setVisible(False)
        self.step_table.horizontalHeader().setVisible(False)
        self.step_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.step_table.hide()

        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.prev_button.clicked.connect(self.show_previous_step)
        self.next_button.clicked.connect(self.show_next_step)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label1)
        main_layout.addWidget(self.label2)
        main_layout.addWidget(self.label3)
        main_layout.addWidget(self.label4)
        main_layout.addWidget(self.step_table)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.current_step = 0
        self.steps = []

    def show_steps(self, win, data1, data2, data3, data4, steps):
        self.label1.setText("Cost: " + data1)
        self.label1.show()
        self.label2.setText("Nodes Expanded: " + data2)
        self.label2.show()
        self.label3.setText("Search Depth: " + data3)
        self.label3.show()
        self.label4.setText("Running Time: " + data4)
        self.label4.show()
        if win.get_flag():
            self.step_table.show()
            self.current_step = 0
            self.steps = steps
            self.show_current_step()
        else:
            self.step_table.hide()

    def show_current_step(self):
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            for i in range(9):
                val = "" if step[i] == '0' else step[i]
                item = QTableWidgetItem(val)
                self.step_table.setItem(i // 3, i % 3, item)

    def show_previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()

    def show_next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    puzzle_app = PuzzleApp()
    puzzle_app.show()
    sys.exit(app.exec_())
