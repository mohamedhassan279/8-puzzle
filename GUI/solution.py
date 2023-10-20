from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPalette, QFont
from PyQt5.QtWidgets import *


class StepDisplayWindow(QWidget):
    def __init__(self, win):
        super().__init__()
        self.wn = win
        self.setWindowTitle("Step Display")
        self.setGeometry(100, 100, 400, 300)

        self.label1 = QLabel()
        self.label1.setStyleSheet("QLabel { color: #03852c; font-weight: bold; font-size: 16px}")
        self.label1.hide()
        self.label2 = QLabel()
        self.label2.setStyleSheet("QLabel { color: #039933; font-weight: bold; font-size: 16px}")
        self.label2.hide()
        self.label3 = QLabel()
        self.label3.setStyleSheet("QLabel { color: #039933; font-weight: bold; font-size: 16px}")
        self.label3.hide()
        self.label4 = QLabel()
        self.label4.setStyleSheet("QLabel { color: #039933; font-weight: bold; font-size: 16px}")
        self.label4.hide()

        self.step_table = QTableWidget(3, 3)
        self.step_table.verticalHeader().setVisible(False)
        self.step_table.horizontalHeader().setVisible(False)
        self.step_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.step_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.step_table.setSelectionMode(QAbstractItemView.NoSelection)

        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.step_table.setFont(font)
        self.step_table.setStyleSheet("""
            QTableWidget::item {
                background-color: transparent;
                color: #754302;
                border: 1.2 solid #a64f08;
            }
            QTableWidget::item:hover {
                background-color: #d99843;
            }
        """)

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
        palette = self.step_table.palette()
        palette.setBrush(QPalette.Base, background_brush)

        # Set the palette for the table
        self.step_table.setPalette(palette)

        for row in range(3):
            for col in range(3):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.TextWordWrap)
                self.step_table.setItem(row, col, item)

        self.step_table.hide()

        self.prev_button = self.create_styled_button("Previous")
        self.next_button = self.create_styled_button("Next")
        self.prev_button.hide()
        self.next_button.hide()
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

        self.step_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        self.current_step = 0
        self.steps = []

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
            self.prev_button.show()
            self.next_button.show()
            self.current_step = 0
            self.steps = steps
            self.show_current_step()
        else:
            self.step_table.hide()
            self.prev_button.hide()
            self.next_button.hide()

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
