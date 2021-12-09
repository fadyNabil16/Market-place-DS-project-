from typing import final
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

USER_WINDOW = {
    'buttons': """
        padding: 10px 10px;
        width: 600px;
        """,
    'main': """
        background-color: white;
    """,
    'txt': """
        color: black;
        font-size: 17px;
        font-weight: bold;
        font-family: Arial;
    """,
    'box': """
        padding: 10px 20px;
    """
}


class UserWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self.user = user
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet(USER_WINDOW['main'])
        self.verticalBox = QVBoxLayout()
        self.verticalBox.addLayout(self.profile())
        self.stack = QStackedWidget()
        self.setLayout(self.verticalBox)
        self.show()

    def profile(self):
        vertical = QVBoxLayout()
        wid_1 = QWidget()
        # wid_1.setStyleSheet(USER_WINDOW[])
        hor_1 = QHBoxLayout()
        hor_2 = QHBoxLayout()
        hor_3 = QHBoxLayout()
        cash = QLabel("Cash")
        cash.setMaximumWidth(40)
        _cash = QLabel("500")
        _cash.setMaximumWidth(100)
        Add = QLabel("Add cash")
        Add.setMaximumWidth(100)
        entry = QLineEdit()
        entry.setMaximumWidth(160)
        _add = QPushButton("Add")
        _add.setMaximumWidth(100)
        for i in [cash, Add, _add, _cash]:
            i.setStyleSheet(USER_WINDOW['txt'])
        hor_2.addWidget(cash)
        hor_2.addWidget(_cash)
        hor_3.addWidget(Add)
        hor_3.addWidget(entry)
        hor_3.addWidget(_add)
        hor_1.addLayout(hor_2)
        hor_1.addLayout(hor_3)
        return hor_1
