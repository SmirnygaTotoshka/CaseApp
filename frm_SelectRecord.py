from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlRelationalTableModel
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QComboBox, QHBoxLayout, QVBoxLayout

import CommonResources


class frm_SelectRecord(QMainWindow):

    def __init__(self,table_name:str,pretty_name:str, parent = None):
        super(frm_SelectRecord, self).__init__(parent)

        self.headers = {
            "tbl_Patients": ["ИД", "Фамилия", "Имя", "Отчество (при наличии)", "Пол", "Дата рождения", "Льготы"
                , "Занятость", "Место работы", "Паспорт", "СНИЛС", "Полис СМО", "Семейное положение", "Телефон"],
            "tbl_Doctors": ["ИД", "Фамилия", "Имя", "Отчество (при наличии)", "Пол", "Дата рождения", "Должность",
                            "Специальность", "Отделение", "Телефон"],
            "tbl_Case": ["ИД", "ИД пациента", "Тип помощи", "Цель", "Результат", "МКБ-10", "Тип заболевания"],
            "tbl_Visit": ["ИД", "ИД доктора", "ИД случая", "Дата", "Место", "Обстоятельства"],
            "tbl_Services": ["ИД", "ИД посещения", "Код", "Тип оплаты"],
            "tbl_Passports": ["ИД", "Серия/номер", "Адрес"],
            "tbl_Polices": ["ИД", "Номер", "СМО"],
        }
        self.setWindowTitle(pretty_name)
        self.widget = QtWidgets.QWidget()
        self.setGeometry(200, 100, CommonResources.screen_width-200, CommonResources.screen_height-200)


        self.b_addData = QtWidgets.QPushButton(self.widget)
        self.b_addData.setText("Добавить")
        self.b_addData.setFont(CommonResources.commonTextFont)
        self.b_addData.setObjectName("addPatient")
        self.b_addData.clicked.connect(self.addData)

        self.b_selectData = QtWidgets.QPushButton(self.widget)
        self.b_selectData.setText("Выбрать")
        self.b_selectData.setFont(CommonResources.commonTextFont)
        self.b_selectData.setObjectName("selectData")
        self.b_selectData.clicked.connect(self.selectData)

        self.tv_Data = QtWidgets.QTableView(self.widget)
        self.tv_Data.setObjectName("tv_Data")
        sizePolicyTable = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicyTable.setHeightForWidth(self.tv_Data.sizePolicy().hasHeightForWidth())
        self.tv_Data.setSizePolicy(sizePolicyTable)

        self.dataModel = QSqlRelationalTableModel()
        self.dataModel.setTable(table_name)
        for i, h in enumerate(self.headers[table_name]):
            self.dataModel.setHeaderData(i, Qt.Horizontal, h)
        self.tv_Data.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tv_Data.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv_Data.horizontalHeader().setCascadingSectionResizes(True)
        self.tv_Data.horizontalHeader().setDefaultSectionSize(200)
        self.tv_Data.horizontalHeader().setMinimumSectionSize(100)
        self.tv_Data.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tv_Data.horizontalHeader().setSortIndicatorShown(True)
        self.tv_Data.horizontalHeader().setStretchLastSection(True)
        self.tv_Data.verticalHeader().setStretchLastSection(False)
        self.tv_Data.setModel(self.dataModel)
        self.dataModel.select()

        self.lookup_Data = QtWidgets.QLineEdit(self.widget)
        self.lookup_Data.setFont(CommonResources.commonTextFont)
        self.lookup_Data.setPlaceholderText("Поиск")
        self.lookup_Data.setMaxLength(100)

        self.dataTypeLookup = QComboBox(self.widget)
        self.dataTypeLookup.addItems(self.headers[table_name])
        self.dataTypeLookup.setFont(CommonResources.commonTextFont)
        # self.dataTypeLookup.currentIndexChanged.connect(self.onEventTypeChanged)
        self.dataTypeLookup.setCurrentIndex(1)

        main_layout = QVBoxLayout()
        up_hLayout = QHBoxLayout()
        down_hLayout = QHBoxLayout()

        up_hLayout.addWidget(self.lookup_Data)
        up_hLayout.addWidget(self.dataTypeLookup)

        down_hLayout.addWidget(self.b_addData)
        down_hLayout.addWidget(self.b_selectData)

        main_layout.addLayout(up_hLayout)
        main_layout.addWidget(self.tv_Data)
        main_layout.addLayout(down_hLayout)
        self.widget.setLayout(main_layout)
        self.setCentralWidget(self.widget)

        self.show()

    def addData(self):
        pass

    def selectData(self):
        pass



# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#
#     def init_res(app):
#         CommonResources.screen = app.primaryScreen()
#         CommonResources.screen_width = CommonResources.screen.availableGeometry().width()
#         CommonResources.screen_height = CommonResources.screen.availableGeometry().height()
#     import sys
#     if CommonResources.database.open():
#         app = QtWidgets.QApplication(sys.argv)
#         init_res(app)
#         window = frm_SelectRecord("tbl_Patients")
#         window.show()
#         sys.exit(app.exec_())
#     else:
#         print("Unable to open data source file.")
#         sys.exit(1)  # Error code 1 - signifies error