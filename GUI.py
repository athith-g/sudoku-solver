# Thanks to https://realpython.com/python-pyqt-gui-calculator/
import sys
from pprint import pprint

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout, QSizePolicy
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtWidgets import QWidget, QFrame
from Solver import Puzzle


def valid():
    for b in boxes:
        if b.text():
            try:
                int(b.text())
            except ValueError:
                b.setText("")
        else:
            b.setStyleSheet("color:black")


def clear(option):
    for b in boxes:
        if option == 0:
            if b.text() == "0":
                b.setStyleSheet("color: black")
                b.setText("")
        if option == 1:
            if "#62e322" in b.styleSheet():
                b.setStyleSheet("color: black")
                b.setText("")
        if option == 2:
                b.setText("")
                b.setStyleSheet("color: black")


def solve():
    p = Puzzle(boxes)
    p.solve_puzzle()

# START APPLICATION
app = QApplication(sys.argv)

# SET WINDOW TITLE AND GRID LAYOUT
window = QWidget()
window.setWindowTitle('Sudoku Solver')
layout = QGridLayout()

# CENTERING THE GRID
layout.setColumnStretch(0, 1)
layout.setColumnStretch(15, 1)
layout.setRowStretch(0, 1)
layout.setRowStretch(16, 1)

# TITLE
layout.addWidget(QLabel('<h1 style="text-align:center;"> Sudoku Solver</h1>', parent=window), 1, 3, 1, 9)

# DRAWING OUT SUDOKU BOXES AND LINES
boxes = {}
for i in range(2, 15):
    solid_line = QFrame()
    solid_line.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

    # Horizontal Lines
    if i == 2 or i == 6 or i == 10 or i == 14:
        for x in range(1, 14):
            button = QPushButton("")
            button.setFixedHeight(3)
            button.setFixedWidth(20) if (x != 1 and x != 13) else button.setFixedWidth(3)
            button.setStyleSheet("background-color: black;")
            layout.addWidget(button, i, x, Qt.AlignHCenter)
    else:
        for j in range(1, 14):
            # Vertical Lines
            if j == 1 or j == 5 or j == 9 or j == 13:
                button = QPushButton("")
                button.setFixedHeight(20)
                button.setFixedWidth(3)
                button.setStyleSheet("background-color: black;")
                layout.addWidget(button, i, j, Qt.AlignHCenter)
            else:
                line = QLineEdit()
                line.setFixedWidth(50)
                line.setFixedHeight(50)
                line.setAlignment(Qt.AlignHCenter)
                line.setMaxLength(1)
                font = line.font()
                font.setPointSize(25)
                line.setFont(font)
                boxes[line] = [i, j]

for box in boxes:
    layout.addWidget(box, boxes[box][0], boxes[box][1], Qt.AlignCenter)
    box.textChanged.connect(valid)

# BUTTONS
button = QPushButton("SOLVE")

font = button.font()
font.setPointSize(25)
font.setBold(True)

button.setFont(font)
button.setMinimumHeight(50)
button.setStyleSheet("Color: green; background-color: black; text-align: center; border-radius: 10px")
button.clicked.connect(solve)
layout.addWidget(button, 15, 1, 1, 4)

button = QPushButton("Clear Zeros")
button.setFont(font)
button.setMinimumHeight(50)
button.setStyleSheet("Color: white; background-color: black; text-align: center; border-radius: 10px")
button.clicked.connect(lambda: clear(0))
layout.addWidget(button, 15, 5, 1, 3)

button = QPushButton("Clear Ansr.")
button.setFont(font)
button.setMinimumHeight(50)
button.setStyleSheet("Color: white; background-color: black; text-align: center; border-radius: 10px")
button.clicked.connect(lambda: clear(1))
layout.addWidget(button, 15, 8, 1, 3)

button = QPushButton("RESET")
button.setFont(font)
button.setMinimumHeight(50)
button.setStyleSheet("Color: red; background-color: black; text-align: center; border-radius: 10px")
button.clicked.connect(lambda: clear(2))
layout.addWidget(button, 15, 11, 1, 4)

# SET LAYOUT AND DISPLAY
window.setLayout(layout)
window.show()

sys.exit(app.exec_())

