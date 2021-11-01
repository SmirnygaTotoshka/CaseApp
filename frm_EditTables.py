from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QAbstractItemView, QHeaderView

import CommonResources
from frm_ActionsWithPatients import frm_ActionsWithPatients

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.commonSetup()
        self.setupTabWidget()

    def commonSetup(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("Учёт амбулаторных посещений (учебная версия)")
        self.setMinimumSize(640, 480)
        self.setMaximumSize(16777215, 16777215)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.globalLayout = QGridLayout(self.centralwidget)
        self.setupTabWidget()
        self.globalLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralwidget)


    def setupTabWidget(self):
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, CommonResources.screen_width, CommonResources.screen_height-30))
        #TODO - write meaning all Polices
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setFont(CommonResources.commonTextFont)
        self.tabWidget.setObjectName("tabWidget")

        self.globalLayout = QVBoxLayout(self.centralwidget)
        self.globalLayout.setContentsMargins(10, 20, 10, 50)
        self.globalLayout.setStretch(0, 0)
        self.globalLayout.addWidget(self.tabWidget)
        self.createCheckReferences()
        self.createPatientsTab()
        self.tabWidget.addTab(self.tab_checkReferences,"")
        self.tabWidget.addTab(self.tab_Patients,"")
        self.tabWidget.setTabText(0,"Проверить справочники")
        self.tabWidget.setTabText(1,"Пациенты")
        self.tabWidget.setCurrentIndex(1)

    def createCheckReferences(self):
        self.tab_checkReferences = QtWidgets.QWidget()
        self.tab_checkReferences.setObjectName("checkReferences")

        self.tv_checkReferences = QtWidgets.QTableView(self.tab_checkReferences)
        #self.tv_checkReferences.setGeometry(QtCore.QRect(100, 200, 1200, 391))
        self.tv_checkReferences.setObjectName("tw_checkReferences")
        sizePolicyTable = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicyTable.setHeightForWidth(self.tv_checkReferences.sizePolicy().hasHeightForWidth())
        self.tv_checkReferences.setSizePolicy(sizePolicyTable)

        self.catalog_type = QComboBox()
        names = self.getTableNames("spr_")
        self.catalog_type.addItems(names)
        #self.catalog_type.move(200, 200)
        #self.catalog_type.currentIndexChanged.connect(self.onEventTypeChanged)
        self.catalog_type.setCurrentIndex(0)

        self.catalogModel = QSqlTableModel()
        self.catalogModel.setTable(names[0])
        self.tv_checkReferences.setModel(self.catalogModel)
        self.tv_checkReferences.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tv_checkReferences.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tv_checkReferences.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv_checkReferences.horizontalHeader().setCascadingSectionResizes(True)
        self.tv_checkReferences.horizontalHeader().setDefaultSectionSize(200)
        self.tv_checkReferences.horizontalHeader().setMinimumSectionSize(100)
        self.tv_checkReferences.horizontalHeader().setSortIndicatorShown(True)
        self.tv_checkReferences.horizontalHeader().setStretchLastSection(True)
        self.tv_checkReferences.verticalHeader().setStretchLastSection(False)
        self.catalog_type.currentIndexChanged.connect(self.onCatalogChanged)
        self.catalogModel.select()

        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(10, 20, 10, 50)
        vLayout.setStretch(0, 0)
        vLayout.addWidget(self.catalog_type)
        vLayout.addWidget(self.tv_checkReferences)
        self.tab_checkReferences.setLayout(vLayout)

    def createPatientsTab(self):
        self.tab_Patients = QtWidgets.QWidget()
        self.tab_Patients.setObjectName("tab_Patients")

        self.b_addPatient = QtWidgets.QPushButton(self.tab_Patients)
        self.b_addPatient.setText("Добавить")
        self.b_addPatient.setFont(CommonResources.commonTextFont)
        #self.b_addPatient.setGeometry(QtCore.QRect(670, 450, 141, 41))
        self.b_addPatient.setObjectName("addPatient")
        self.b_addPatient.clicked.connect(self.addPatient)

        self.b_deletePatient = QtWidgets.QPushButton(self.tab_Patients)
        #self.b_deletePatient.setGeometry(QtCore.QRect(10, 420, 291, 51))
        self.b_deletePatient.setText("Удалить")
        self.b_deletePatient.setFont(CommonResources.commonTextFont)
        self.b_deletePatient.clicked.connect(self.deletePatient)
        self.b_deletePatient.setObjectName("deletePatient")

        self.b_updatePatient = QtWidgets.QPushButton(self.tab_Patients)
        self.b_updatePatient.setText("Редактировать")
        self.b_updatePatient.setFont(CommonResources.commonTextFont)
        #QWidget.b_updatePatient.setGeometry(QtCore.QRect(10, 480, 291, 51))
        self.b_updatePatient.setObjectName("updatePatient")
        self.b_updatePatient.clicked.connect(self.updatePatient)

        self.tv_Patients = QtWidgets.QTableView(self.tab_Patients)
        # self.tv_Patients.setGeometry(QtCore.QRect(100, 200, 1200, 391))
        self.tv_Patients.setObjectName("tw_checkReferences")
        sizePolicyTable = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicyTable.setHeightForWidth(self.tv_Patients.sizePolicy().hasHeightForWidth())
        self.tv_Patients.setSizePolicy(sizePolicyTable)

        self.patientsModel = QSqlTableModel()
        self.patientsModel.setTable("tbl_Patients")
        headers = ["ИД","Фамилия","Имя","Отчество (при наличии)","Пол","Дата рождения","Льготы"
                                             ,"Занятость","Место работы","Паспорт","СНИЛС","Полис СМО","Семейное положение","Телефон"]
        for i,h in enumerate(headers):
            self.patientsModel.setHeaderData(i, Qt.Horizontal,h)
        self.tv_Patients.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tv_Patients.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv_Patients.horizontalHeader().setCascadingSectionResizes(True)
        self.tv_Patients.horizontalHeader().setDefaultSectionSize(200)
        self.tv_Patients.horizontalHeader().setMinimumSectionSize(100)
        self.tv_Patients.horizontalHeader().setSortIndicatorShown(True)
        self.tv_Patients.horizontalHeader().setStretchLastSection(True)
        self.tv_Patients.verticalHeader().setStretchLastSection(False)
        self.tv_Patients.setModel(self.patientsModel)
        self.patientsModel.select()

        self.lookup_Patients = QtWidgets.QLineEdit(self.tab_Patients)
        #QWidget.lookup.move(100, 20)
        self.lookup_Patients.setFont(CommonResources.commonTextFont)
        self.lookup_Patients.setPlaceholderText("Поиск")
        self.lookup_Patients.setMaxLength(100)

        self.patientTypeLookup = QComboBox()
        self.patientTypeLookup.addItems(headers)
        #QWidget.event_type.move(200, 20)
        #self.patientTypeLookup.currentIndexChanged.connect(self.onEventTypeChanged)
        self.patientTypeLookup.setCurrentIndex(0)

        main_layout = QVBoxLayout()
        up_hLayout = QHBoxLayout()
        down_hLayout = QHBoxLayout()

        up_hLayout.addWidget(self.lookup_Patients)
        up_hLayout.addWidget(self.patientTypeLookup)

        down_hLayout.addWidget(self.b_addPatient)
        down_hLayout.addWidget(self.b_updatePatient)
        down_hLayout.addWidget(self.b_deletePatient)

        main_layout.addLayout(up_hLayout)
        main_layout.addWidget(self.tv_Patients)
        main_layout.addLayout(down_hLayout)
        self.tab_Patients.setLayout(main_layout)

    def onCatalogChanged(self,index):
        names = self.getTableNames("spr_")
        self.catalogModel.setTable(names[index])
        self.catalogModel.select()

    def addPatient(self):
        self.rec = frm_ActionsWithPatients(action = frm_ActionsWithPatients.ADD, model = None, parent = self)

    def deletePatient(self):
        pass

    def updatePatient(self):
        pass

    def getTableNames(self,name:str) -> list:
        names = []
        for n in CommonResources.database.tables():
            if name in n:
                names.append(n)
        return names

    def getColumns(self,name: str) -> list:
        table_names = QSqlQuery()
        table_names.prepare("SELECT COLUMN_NAME FROM ambulatoryCase.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=?")
        table_names.addBindValue(name)
        table_names.exec_()
        names = []
        while (table_names.next()):
            s = table_names.value(0)
            names.append(s)
        return names