import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, \
    QHBoxLayout, QHeaderView, QAbstractItemView

import main


class PuzzleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Puzzle Solver")
        self.setGeometry(500, 200, 800, 600)

        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)

        self.table_widget = QTableWidget(3, 3)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)

        self.submit_button1 = self.create_styled_button("BFS")
        self.submit_button2 = self.create_styled_button("DFS")
        self.submit_button3 = self.create_styled_button("A*(Manhattan)")
        self.submit_button4 = self.create_styled_button("A*(Euclidean)")

        self.on_off_button = self.create_styled_button("On/Off Steps", checkable=True)
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

        self.central_layout.addWidget(self.table_widget)
        self.central_layout.addLayout(button_layout)
        self.central_layout.addWidget(self.on_off_button)

        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        self.update_row_heights()
        self.resizeEvent = self.custom_resize_event

        # Initialize the step display window
        self.step_display_window = StepDisplayWindow()

    def custom_resize_event(self, event):
        self.update_row_heights()
        super(PuzzleApp, self).resizeEvent(event)

    def update_row_heights(self):
        height = self.table_widget.height() // self.table_widget.rowCount()
        for row in range(self.table_widget.rowCount()):
            self.table_widget.setRowHeight(row, height)

    def toggle_steps(self):
        if self.on_off_button.isChecked():
            # Steps are on.
            pass  # Implement your logic here to enable steps
        else:
            # Steps are off.
            pass  # Implement your logic here to disable steps

    def solve(self, fun):
        start = self.read_table_input()
        if not main.is_solvable(start):
            print("Non Solvable")
            return
        start_time = time.time()
        ans = fun(start)
        end_time = time.time()
        exec_time = end_time - start_time
        print("Finished in:", round(exec_time * 1e3, 4), "ms")
        trace = main.get_path(ans)
        trace.reverse()
        self.step_display_window.show()
        self.step_display_window.show_steps(trace)
        print(trace)

    def method1(self):
        self.solve(main.bfs)

    def method2(self):
        self.solve(main.dfs)

    def method3(self):
        self.solve(main.Astar)

    def method4(self):
        self.solve(main.Astar)

    def read_table_input(self):
        puzzle_input = ""
        for row in range(self.table_widget.rowCount()):
            row_values = ""
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item:
                    value = item.text()
                    if not value:
                        value = "0"
                    row_values += value
            puzzle_input += row_values
        return puzzle_input

    def create_styled_button(self, text, checkable=False):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                border: none;
                color: white;
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


class StepDisplayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Step Display")
        self.setGeometry(100, 100, 400, 300)

        self.step_table = QTableWidget(3, 3)
        self.step_table.verticalHeader().setVisible(False)
        self.step_table.horizontalHeader().setVisible(False)
        self.step_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.prev_button.clicked.connect(self.show_previous_step)
        self.next_button.clicked.connect(self.show_next_step)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.step_table)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.current_step = 0
        self.steps = []

    def show_steps(self, steps):
        print("show")
        self.current_step = 0
        self.steps = steps
        self.show_current_step()

    def show_current_step(self):
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            for i in range(9):
                item = QTableWidgetItem(step[i])
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
