from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QFormLayout

import EditDBFormFactory as eff
import EditDBFormControllerMethods as controller
from frm_SelectRecord import frm_SelectRecord


class frm_ActionsWithData(QMainWindow):
    ADD = 1
    UPDATE = 2
    '''
    action - режим работы
    tbl_name - имя таблицы, для которой производится действие с данными
    label_dict - key:value from db, value - russian equivalent 
    model - QSqlModel contains data
    '''
    def __init__(self,action:int,table_name:str, model:QSqlTableModel, index = -1,parent = None):
        super(frm_ActionsWithData, self).__init__(parent)
        self.parent = parent
        if action == self.UPDATE and index == -1:
            raise Exception("I don`t know record which I`ve to work from table tbl_Patients")
        if action != self.UPDATE and action != self.ADD:
            raise Exception("Wrong action with data from table tbl_Patients")
        self.table_name = table_name
        self.action = action
        self.model = model
        self.index = index
        self.setGeometry(100, 100, 700, 600)
        if action == self.ADD:
            self.setWindowTitle('Добавить запись в базу данных')
        elif action == self.UPDATE:
            self.setWindowTitle('Редактирование записи из базы данных')
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

    def addPassport(self):
        self.recPassport = frm_SelectRecord("tbl_Passports","Паспорта", self)

    def addPolice(self):
        self.recPolice = frm_SelectRecord("tbl_Polices", "Полисы", self)

    def selectPatient(self):
        pass

    def selectDoctor(self):
        pass

    def selectCase(self):
        pass

    def selectVisit(self):
        pass

    def prettyPassportPrint(self, text):
        if len(text) == 4:
            self.number.setText(text + " ")

    def closeEvent(self, event):
        self.parent.switchEnablingEditingActions(True)#TODO dangerous
    #self.parent.switc(True)
