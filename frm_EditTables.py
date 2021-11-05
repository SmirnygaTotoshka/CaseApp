from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlTableModel, QSqlRelationalTableModel, QSqlRelation
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QAbstractItemView, QHeaderView

import CommonResources
from frm_ActionsWithData import frm_ActionsWithData

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.prettyTableNames = {
            "Пациенты" : "tbl_Patients",
            "Доктора" : "tbl_Doctors",
            "Случаи" : "tbl_Case",
            "Посещения" : "tbl_Visit",
            "Услуги" : "tbl_Services",
            "Паспорта" : "tbl_Passports",
            "Полисы" : "tbl_Polices"
        }
        self.headers = {
            "tbl_Patients" : ["ИД","Фамилия","Имя","Отчество (при наличии)","Пол","Дата рождения","Льготы"
                                             ,"Занятость","Место работы","Паспорт","СНИЛС","Полис СМО","Семейное положение","Телефон"],
            "tbl_Doctors" : ["ИД","Фамилия","Имя","Отчество (при наличии)","Пол","Дата рождения","Должность","Специальность","Отделение", "Телефон"],
            "tbl_Case" : ["ИД","ИД пациента","Тип помощи","Цель","Результат","МКБ-10","Тип заболевания"],
            "tbl_Visit" : ["ИД","ИД доктора","ИД случая","Дата","Место","Обстоятельства"],
            "tbl_Services" : ["ИД", "ИД посещения", "Код", "Тип оплаты"],
            "tbl_Passports" : ["ИД", "Серия/номер", "Адрес"],
            "tbl_Polices" : ["ИД", "Номер", "СМО"],
        }

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
        self.createDataTab()
        self.tabWidget.addTab(self.tab_checkReferences,"")
        self.tabWidget.addTab(self.tab_Data, "")
        self.tabWidget.setTabText(0,"Проверить справочники")
        self.tabWidget.setTabText(1,"Данные")
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
        self.tv_checkReferences.setEditTriggers(QAbstractItemView.NoEditTriggers)
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

    def createDataTab(self):
        self.tab_Data = QtWidgets.QWidget()
        self.tab_Data.setObjectName("tab_Patients")

        self.b_addData = QtWidgets.QPushButton(self.tab_Data)
        self.b_addData.setText("Добавить")
        self.b_addData.setFont(CommonResources.commonTextFont)
        self.b_addData.setObjectName("addPatient")
        self.b_addData.clicked.connect(self.addData)

        self.b_deleteData = QtWidgets.QPushButton(self.tab_Data)
        self.b_deleteData.setText("Удалить")
        self.b_deleteData.setFont(CommonResources.commonTextFont)
        self.b_deleteData.clicked.connect(self.deleteData)
        self.b_deleteData.setObjectName("deletePatient")

        self.b_updateData = QtWidgets.QPushButton(self.tab_Data)
        self.b_updateData.setText("Редактировать")
        self.b_updateData.setFont(CommonResources.commonTextFont)
        self.b_updateData.setObjectName("updatePatient")
        self.b_updateData.clicked.connect(self.updateData)

        self.tv_Data = QtWidgets.QTableView(self.tab_Data)
        self.tv_Data.setObjectName("tv_Data")
        sizePolicyTable = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicyTable.setHeightForWidth(self.tv_Data.sizePolicy().hasHeightForWidth())
        self.tv_Data.setSizePolicy(sizePolicyTable)

        self.dataModel = QSqlRelationalTableModel()
        self.dataModel.setTable("tbl_Patients")
        self.dataModel.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)
        self.dataModel.sort(0, 0)  # DEFAULT SORT TO SEE NEW ITEMS AT END
        for i,h in enumerate(self.headers["tbl_Patients"]):
            self.dataModel.setHeaderData(i, Qt.Horizontal, h)

        self.dataModel.setRelation(self.dataModel.fieldIndex("PassportID"), QSqlRelation('tbl_Passports', 'UniqueID', 'Number'))
        self.dataModel.setRelation(self.dataModel.fieldIndex("PoliceID"), QSqlRelation('tbl_Polices', 'UniqueID', 'Number'))
        self.tv_Data.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tv_Data.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv_Data.horizontalHeader().setCascadingSectionResizes(True)
        self.tv_Data.horizontalHeader().setDefaultSectionSize(200)
        self.tv_Data.horizontalHeader().setMinimumSectionSize(100)
        self.tv_Data.horizontalHeader().setSortIndicatorShown(True)
        self.tv_Data.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tv_Data.horizontalHeader().setStretchLastSection(True)
        self.tv_Data.verticalHeader().setStretchLastSection(False)
        self.tv_Data.setModel(self.dataModel)
        self.dataModel.select()

        self.lookup_Data = QtWidgets.QLineEdit(self.tab_Data)
        self.lookup_Data.setFont(CommonResources.commonTextFont)
        self.lookup_Data.setPlaceholderText("Поиск")
        self.lookup_Data.setMaxLength(100)

        self.dataTypeLookup = QComboBox()
        self.dataTypeLookup.addItems(self.headers["tbl_Patients"])
        #self.dataTypeLookup.currentIndexChanged.connect(self.onEventTypeChanged)
        self.dataTypeLookup.setCurrentIndex(1)

        self.selectTable = QComboBox()
        self.selectTable.addItems(list(self.prettyTableNames.keys()))
        for i,k in enumerate(self.prettyTableNames.keys()):
            self.selectTable.setItemData(i, self.prettyTableNames[k], Qt.UserRole)
        self.selectTable.currentIndexChanged.connect(self.onTableChanged)
        self.selectTable.setCurrentIndex(0)

        main_layout = QVBoxLayout()
        up_hLayout = QHBoxLayout()
        down_hLayout = QHBoxLayout()

        up_hLayout.addWidget(self.lookup_Data)
        up_hLayout.addWidget(self.dataTypeLookup)

        down_hLayout.addWidget(self.b_addData)
        down_hLayout.addWidget(self.b_updateData)
        down_hLayout.addWidget(self.b_deleteData)

        main_layout.addWidget(self.selectTable)
        main_layout.addLayout(up_hLayout)
        main_layout.addWidget(self.tv_Data)
        main_layout.addLayout(down_hLayout)
        self.tab_Data.setLayout(main_layout)

    def onCatalogChanged(self,index):
        names = self.getTableNames("spr_")
        self.catalogModel.setTable(names[index])
        self.catalogModel.select()

    def onTableChanged(self,index):
        table_name = self.selectTable.itemData(index,Qt.UserRole)
        self.dataModel.setTable(table_name)
        if table_name == "tbl_Polices":
            index = self.dataModel.fieldIndex("Organization")
            rel = QSqlRelation('spr_SMO', 'ID', 'NAM_SMOP')
            self.dataModel.setRelation(index,rel)
        for i, h in enumerate(self.headers[table_name]):
            self.dataModel.setHeaderData(i, Qt.Horizontal, h)
        self.tv_Data.setModel(self.dataModel)
        self.dataModel.select()
        self.dataTypeLookup.clear()
        self.dataTypeLookup.addItems(self.headers[table_name])


    def addData(self):
        table_name = self.selectTable.currentData(Qt.UserRole)
        self.setVisible(False)
        self.rec = frm_ActionsWithData(action = frm_ActionsWithData.ADD, table_name = table_name,model = self.dataModel, parent = self)

    def deleteData(self):
        pass

    def updateData(self):
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