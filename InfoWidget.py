from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QSizePolicy, QHBoxLayout

import CommonResources


class InfoAfterSelectWidget(QWidget):

    def __init__(self, parent = None, text = ""):
        super(InfoAfterSelectWidget, self).__init__(parent)

        self.title = QLabel()
        self.title.setFont(CommonResources.commonTextFont)
        self.title.setText(text)
        self.title.setWordWrap(True)

        self.change = QPushButton()
        self.change.setText("Изменить")  # TODO - проверка на наличие
        self.change.setFont(CommonResources.commonTextFont)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)

        lay.addWidget(self.title)
        lay.addWidget(self.change)

    def connectButton(self, method):
        self.change.clicked.connect(method)
        
    def setTitleText(self, text):
        self.title.setText(text)

    def getText(self):
        return self.title.text()
