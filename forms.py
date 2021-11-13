from PyQt5.QtCore import Qt, QRect
from PyQt5.QtSql import QSqlTableModel, QSqlRelation, QSqlRelationalTableModel, QSqlQuery
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QFormLayout, QMessageBox, QLabel, QPushButton, \
    QSizePolicy, QTableView, QAbstractItemView, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, \
    QHeaderView

import CommonResources
import EditDBFormFactory as eff
import EditDBFormControllerMethods as controller
from InfoWidget import InfoAfterSelectWidget


class frm_EditRecord(QMainWindow):
    '''
    action - режим работы
    tbl_name - имя таблицы, для которой производится действие с данными
    label_dict - key:value from db, value - russian equivalent 
    model - QSqlModel contains data
    '''
    def __init__(self,action:int,table_name:str, model:QSqlTableModel,parent = None):
        super(frm_EditRecord, self).__init__(parent)
        self.parent = parent

        self.table_name = table_name
        self.action = action
        self.model = model
        self.setGeometry(100, 100, 700, 600)
        if action == CommonResources.ADD:
            self.setWindowTitle('Добавить запись в базу данных')
        elif action == CommonResources.UPDATE:
            self.setWindowTitle('Редактирование записи из базы данных')
        if action == CommonResources.UPDATE and not self.parent.tv_Data.selectionModel().hasSelection():
            raise Exception("Выберите запись.")
        if action != CommonResources.UPDATE and action != CommonResources.ADD:
            raise Exception("Неизвестное действие над данными")
        self.initUI(action)


    def initUI(self,action):
        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.form = QFormLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        self.form.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.form.setSpacing(1)
        if self.table_name == "tbl_Patients":
            eff.createPatientForm(self,action)
        elif self.table_name == "tbl_Doctors":
            eff.createDoctorForm(self,action)
        elif self.table_name == "tbl_Case":
            eff.createCaseForm(self,action)
        elif self.table_name == "tbl_Visit":
            eff.createVisitForm(self,action)
        elif self.table_name == "tbl_Services":
            eff.createServicesForm(self,action)
        elif self.table_name == "tbl_Passports":
            eff.createPassportForm(self,action)
        elif self.table_name == "tbl_Polices":
            eff.createPoliceForm(self,action)
        else:
            raise Exception("Wrong table name = " + self.table_name)

        self.widget.setLayout(self.form)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.scroll.setWidgetResizable(False)
        self.show()

    def checkPriviledge(self, state):
        if state == Qt.Checked:
            self.priviledge.setEnabled(True)
        else:
            self.priviledge.setEnabled(False)

    def SavingResult(self):
        if self.table_name == "tbl_Patients":
            f = controller.savePatient(self,self.action)
        elif self.table_name == "tbl_Doctors":
            f = controller.saveDoctor(self,self.action)
        elif self.table_name == "tbl_Case":
            f = controller.saveCase(self,self.action)
        elif self.table_name == "tbl_Visit":
            f = controller.saveVisit(self,self.action)
        elif self.table_name == "tbl_Services":
            f = controller.saveServices(self,self.action)
        elif self.table_name == "tbl_Passports":
            f = controller.savePassports(self,self.action)
        elif self.table_name == "tbl_Polices":
            f = controller.savePolices(self,self.action)
        if f:
            self.close()

    def SirnamefirstToUpper(self, text):
        self.Sirname.setText(text.capitalize())

    def NamefirstToUpper(self, text):
        self.Name.setText(text.capitalize())

    def SecondNamefirstToUpper(self, text):
        self.SecondName.setText(text.capitalize())


    def selectPassport(self):
        self.recPassport = frm_SelectRecord("tbl_Passports","Паспорта", self)
        self.save.setEnabled(False)

    def selectPolice(self):
        self.recPolice = frm_SelectRecord("tbl_Polices", "Полисы", self)
        self.save.setEnabled(False)

    def selectPatient(self):
        self.recPatient = frm_SelectRecord("tbl_Patients", "Пациенты", self)
        self.save.setEnabled(False)

    def selectDoctor(self):
        self.recDoctor = frm_SelectRecord("tbl_Doctors", "Доктора", self)
        self.save.setEnabled(False)

    def selectCase(self):
        self.recCase = frm_SelectRecord("tbl_Case", "Случаи", self)
        self.save.setEnabled(False)

    def selectVisit(self):
        self.recVisit = frm_SelectRecord("tbl_Visit", "Посещения", self)
        self.save.setEnabled(False)

    def prettyPassportPrint(self, text):
        if len(text) == 4:
            self.number.setText(text + " ")

    def closeEvent(self, event):
        self.parent.switchEnablingEditingActions(True)#TODO dangerous
    #self.parent.switc(True)

class frm_MainWindow(QMainWindow):

    def __init__(self):
        super(frm_MainWindow, self).__init__()
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
            "tbl_Case" : ["ИД","ИД пациента","Тип помощи","Цель","Результат","Код МКБ-10","Тип заболевания"],
            "tbl_Visit" : ["ИД","ИД доктора","ИД случая","Дата","Место","Обстоятельства"],
            "tbl_Services" : ["ИД", "ИД посещения", "Услуга", "Тип оплаты"],
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
        self.setWindowState(Qt.WindowMaximized)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.globalLayout = QGridLayout(self.centralwidget)
        self.setupTabWidget()
        self.globalLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralwidget)


    def setupTabWidget(self):
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QRect(0, 0, CommonResources.screen_width, CommonResources.screen_height-30))
        #TODO - write meaning all Polices
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        self.tab_checkReferences = QWidget()
        self.tab_checkReferences.setObjectName("checkReferences")

        self.tv_checkReferences = QTableView(self.tab_checkReferences)
        #self.tv_checkReferences.setGeometry(QtCore.QRect(100, 200, 1200, 391))
        self.tv_checkReferences.setObjectName("tw_checkReferences")
        sizePolicyTable = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        self.tab_Data = QWidget()
        self.tab_Data.setObjectName("tab_Patients")

        self.b_addData = QPushButton(self.tab_Data)
        self.b_addData.setText("Добавить")
        self.b_addData.setFont(CommonResources.commonTextFont)
        self.b_addData.setObjectName("addPatient")
        self.b_addData.clicked.connect(self.addData)

        self.b_deleteData = QPushButton(self.tab_Data)
        self.b_deleteData.setText("Удалить")
        self.b_deleteData.setFont(CommonResources.commonTextFont)
        self.b_deleteData.clicked.connect(self.deleteData)
        self.b_deleteData.setObjectName("deletePatient")

        self.b_updateData = QPushButton(self.tab_Data)
        self.b_updateData.setText("Редактировать")
        self.b_updateData.setFont(CommonResources.commonTextFont)
        self.b_updateData.setObjectName("updatePatient")
        self.b_updateData.clicked.connect(self.updateData)

        self.tv_Data = QTableView(self.tab_Data)
        self.tv_Data.setObjectName("tv_Data")
        sizePolicyTable = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicyTable.setHeightForWidth(self.tv_Data.sizePolicy().hasHeightForWidth())
        self.tv_Data.setSizePolicy(sizePolicyTable)

        self.dataModel = QSqlRelationalTableModel()
        self.dataModel.setTable("tbl_Patients")
        fIndex = ["Sex","Priviledge","Employment","PassportID", "PoliceID","FamilyStatus"]
        spr = ['spr_Sex',"spr_Priviledge","spr_Employment","tbl_Passports","tbl_Polices","spr_FamilyStatus"]
        cols = ["NAME","NAME","NAME","Number", "Number","NAME"]
        self.setRelations(fIndex, spr, cols)
        self.dataModel.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)
        self.dataModel.sort(0, 0)  # DEFAULT SORT TO SEE NEW ITEMS AT END
        for i,h in enumerate(self.headers["tbl_Patients"]):
            self.dataModel.setHeaderData(i, Qt.Horizontal, h)
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

        self.lookup_Data = QLineEdit(self.tab_Data)
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
        if table_name == "tbl_Patients":
            fIndex = ["Sex", "Priviledge", "Employment", "PassportID", "PoliceID", "FamilyStatus"]
            spr = ['spr_Sex', "spr_Priviledge", "spr_Employment", "tbl_Passports", "tbl_Polices", "spr_FamilyStatus"]
            cols = ["NAME", "NAME", "NAME", "Number", "Number", "NAME"]
            self.setRelations(fIndex, spr, cols)
        if table_name == "tbl_Doctors":
            fIndex = ["Sex","Position","Speciality","Department"]
            spr = ['spr_Sex','spr_Positions','spr_Speciality','spr_Departments']
            cols = ['NAME']*4
            self.setRelations(fIndex,spr,cols)
        if table_name == "tbl_Case":
            fIndex = ["AidType","Purpose","Result","DiagnosisCode","DiseaseType"]
            spr = ['spr_AidType','spr_Purpose','spr_Result','spr_MKB','spr_DiseaseType']
            cols = ['NAME','NAME','NAME','MKB_CODE','NAME']
            self.setRelations(fIndex,spr,cols)
        if table_name == "tbl_Visit":
            fIndex = ["VisitPlace","Circumstance"]
            spr = ['spr_VisitPlace','spr_VisitCircumstances']
            cols = ['NAME','NAME']
            self.setRelations(fIndex,spr,cols)
        if table_name == "tbl_Services":
            fIndex = ["Code","PaymentType"]
            spr = ['spr_CodeServices','spr_PaymentType']
            cols = ['NAME','FULL_NAME']
            self.setRelations(fIndex,spr,cols)
        if table_name == "tbl_Polices":
            self.setRelations(["Organization"], ['spr_SMO'], ['NAM_SMOP'])

        for i, h in enumerate(self.headers[table_name]):
            self.dataModel.setHeaderData(i, Qt.Horizontal, h)
        self.tv_Data.setModel(self.dataModel)
        self.dataModel.select()
        self.dataTypeLookup.clear()
        self.dataTypeLookup.addItems(self.headers[table_name])


    def addData(self):
        table_name = self.selectTable.currentData(Qt.UserRole)
        self.switchEnablingEditingActions(False)
        try:
            self.rec = frm_EditRecord(action = CommonResources.ADD, table_name = table_name, model = self.dataModel, parent = self)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", e, QMessageBox.Ok)

    def deleteData(self):
        rows = self.tv_Data.selectionModel().selectedRows()
        if len(rows) == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись.", QMessageBox.Ok)
        else:
            for r in rows:
                self.dataModel.deleteRowFromTable(r.row())
            self.dataModel.select()

    def updateData(self):
        table_name = self.selectTable.currentData(Qt.UserRole)
        self.switchEnablingEditingActions(False)
        try:
            self.rec = frm_EditRecord(action=CommonResources.UPDATE, table_name=table_name, model=self.dataModel,
                                      parent=self)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", e, QMessageBox.Ok)


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

    def switchEnablingEditingActions(self,flag):
        self.b_addData.setEnabled(flag)
        self.b_deleteData.setEnabled(flag)
        self.b_updateData.setEnabled(flag)
        self.selectTable.setEnabled(flag)

    def setRelations(self, fieldIndex, table_name, col_name):
        for f,t,c in zip(fieldIndex,table_name,col_name):
            index = self.dataModel.fieldIndex(f)
            rel = QSqlRelation(t, 'ID', c)
            self.dataModel.setRelation(index, rel)


class frm_SelectRecord(QMainWindow):

    def __init__(self,table_name:str,pretty_name:str, parent = None):
        super(frm_SelectRecord, self).__init__(parent)
        self.parent = parent
        self.headers = {
            "tbl_Patients": ["ИД", "Фамилия", "Имя", "Отчество (при наличии)", "Пол", "Дата рождения", "Льготы"
                , "Занятость", "Место работы", "Паспорт", "СНИЛС", "Полис СМО", "Семейное положение", "Телефон"],
            "tbl_Doctors": ["ИД", "Фамилия", "Имя", "Отчество (при наличии)", "Пол", "Дата рождения", "Должность",
                            "Специальность", "Отделение", "Телефон"],
            "tbl_Case": ["ИД", "ИД пациента", "Тип помощи", "Цель", "Результат", "МКБ-10", "Тип заболевания"],
            "tbl_Visit": ["ИД", "ИД доктора", "ИД случая", "Дата", "Место", "Обстоятельства"],
            "tbl_Services": ["ИД", "ИД посещения", "Услуга", "Тип оплаты"],
            "tbl_Passports": ["ИД", "Серия/номер", "Адрес"],
            "tbl_Polices": ["ИД", "Номер", "СМО"],
        }
        self.setWindowTitle(pretty_name)
        self.widget = QWidget()
        self.setGeometry(200, 100, CommonResources.screen_width-200, CommonResources.screen_height-200)
        self.table_name = table_name

        self.b_selectData = QPushButton(self.widget)
        self.b_selectData.setText("Выбрать")
        self.b_selectData.setFont(CommonResources.commonTextFont)
        self.b_selectData.setObjectName("selectData")
        self.b_selectData.clicked.connect(self.selectData)

        self.tv_Data = QTableView(self.widget)
        self.tv_Data.setObjectName("tv_Data")
        sizePolicyTable = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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

        self.lookup_Data = QLineEdit(self.widget)
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

        down_hLayout.addWidget(self.b_selectData)

        main_layout.addLayout(up_hLayout)
        main_layout.addWidget(self.tv_Data)
        main_layout.addLayout(down_hLayout)
        self.widget.setLayout(main_layout)
        self.setCentralWidget(self.widget)

        self.show()

    def switchEnablingEditingActions(self,flag):
        self.b_selectData.setEnabled(flag)

    def selectData(self):
        if self.tv_Data.selectionModel().hasSelection():
            if self.table_name == "tbl_Passports":
                row = self.tv_Data.selectionModel().selectedRows()
                passport = self.dataModel.data(self.dataModel.index(row[0].row(), 1))
                self.parent.selected_passport = InfoAfterSelectWidget(text = passport)
                self.parent.selected_passport.change.clicked.connect(self.parent.selectPassport)
                self.parent.form.removeRow(9)
                title = QLabel("Паспорт")
                title.setFont(CommonResources.commonTextFont)
                self.parent.form.insertRow(9,title, self.parent.selected_passport)
                self.close()
            elif self.table_name == "tbl_Polices":
                row = self.tv_Data.selectionModel().selectedRows()
                police = self.dataModel.data(self.dataModel.index(row[0].row(), 1))
                self.parent.selected_police = InfoAfterSelectWidget(text=police)
                self.parent.selected_police.change.clicked.connect(self.parent.selectPolice)
                self.parent.form.removeRow(11)
                title = QLabel("Паспорт")
                title.setFont(CommonResources.commonTextFont)
                self.parent.form.insertRow(11, title, self.parent.selected_police)
                self.close()
            elif self.table_name == "tbl_Patients":
                row = self.tv_Data.selectionModel().selectedRows()
                patient = str(self.dataModel.data(self.dataModel.index(row[0].row(), 0))) + " " +str(self.dataModel.data(self.dataModel.index(row[0].row(), 1))) + " " + str(self.dataModel.data(self.dataModel.index(row[0].row(), 2))) + " " +str(self.dataModel.data(self.dataModel.index(row[0].row(), 3)))
                self.parent.selected_patient = InfoAfterSelectWidget(text=patient)
                self.parent.selected_patient.change.clicked.connect(self.parent.selectPatient)
                self.parent.form.removeRow(0)
                title = QLabel("Пациент")
                title.setFont(CommonResources.commonTextFont)
                self.parent.form.insertRow(0, title, self.parent.selected_patient)
                self.close()
            elif self.table_name == "tbl_Doctors":
                row = self.tv_Data.selectionModel().selectedRows()
                patient = str(self.dataModel.data(self.dataModel.index(row[0].row(), 0))) + " " +str(self.dataModel.data(self.dataModel.index(row[0].row(), 1))) + " " + str(self.dataModel.data(self.dataModel.index(row[0].row(), 2))) + " " +str(self.dataModel.data(self.dataModel.index(row[0].row(), 3)))
                self.parent.selected_doctor = InfoAfterSelectWidget(text=patient)
                self.parent.selected_doctor.change.clicked.connect(self.parent.selectDoctor)
                self.parent.form.removeRow(0)
                title = QLabel("Доктор")
                title.setFont(CommonResources.commonTextFont)
                self.parent.form.insertRow(0, title, self.parent.selected_doctor)
                self.close()
            elif self.table_name == "tbl_Case":
                row = self.tv_Data.selectionModel().selectedRows()
                case = str(self.dataModel.data(self.dataModel.index(row[0].row(), 0)))
                self.parent.selected_case = InfoAfterSelectWidget(text=case)
                self.parent.selected_case.change.clicked.connect(self.parent.selectCase)
                self.parent.form.removeRow(1)
                title = QLabel("Случай")
                title.setFont(CommonResources.commonTextFont)
                self.parent.form.insertRow(1, title, self.parent.selected_case)
                self.close()
            elif self.table_name == "tbl_Visit":
                row = self.tv_Data.selectionModel().selectedRows()
                visit = str(self.dataModel.data(self.dataModel.index(row[0].row(), 0)))
                self.parent.selected_visit = InfoAfterSelectWidget(text=visit)
                self.parent.selected_visit.change.clicked.connect(self.parent.selectVisit)
                self.parent.form.removeRow(0)
                title = QLabel("Посещение")
                title.setFont(CommonResources.commonTextFont)
                self.parent.form.insertRow(0, title, self.parent.selected_visit)
                self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите запись", QMessageBox.Ok)

    def closeEvent(self, a0) -> None:
        self.parent.save.setEnabled(True)




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