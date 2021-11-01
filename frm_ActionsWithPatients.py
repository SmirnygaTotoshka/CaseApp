from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QFormLayout, QLabel, QLineEdit, QComboBox, QDateTimeEdit, \
    QPushButton, QCheckBox

import CommonResources


class frm_ActionsWithPatients(QMainWindow):
    ADD = 1
    UPDATE = 2
    '''
    action - режим работы
    tbl_name - имя таблицы, для которой производится действие с данными
    label_dict - key:value from db, value - russian equivalent 
    model - QSqlModel contains data
    '''
    def __init__(self,action:int, model:QSqlTableModel, index = -1,parent = None):
        super(frm_ActionsWithPatients,self).__init__(parent)
        if action == self.UPDATE and index == -1:
            raise Exception("I don`t know record which I`ve to work from table tbl_Patients")
        if action != self.UPDATE and action != self.ADD:
            raise Exception("Wrong action with data from table tbl_Patients")

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
        title = QLabel("Фамилия")
        title.setFont(CommonResources.commonTextFont)

        self.Sirname = QLineEdit()
        self.Sirname.setFont(CommonResources.commonTextFont)
        self.Sirname.setMaxLength(50)
        self.Sirname.setValidator(QRegExpValidator(CommonResources.only_letter, self.Sirname))
        self.Sirname.setObjectName("Sirname")
        self.Sirname.textEdited.connect(self.SirnamefirstToUpper)
        self.form.addRow(title, self.Sirname)

        title = QLabel("Имя")
        title.setFont(CommonResources.commonTextFont)

        self.Name = QLineEdit()
        self.Name.setFont(CommonResources.commonTextFont)
        self.Name.setMaxLength(50)
        self.Name.setValidator(QRegExpValidator(CommonResources.only_letter, self.Name))
        self.Name.setObjectName("Name")
        self.Name.textEdited.connect(self.NamefirstToUpper)
        self.form.addRow(title, self.Name)

        title = QLabel("Отчество (при наличии)")
        title.setFont(CommonResources.commonTextFont)

        self.SecondName = QLineEdit()
        self.SecondName.setFont(CommonResources.commonTextFont)
        self.SecondName.setMaxLength(50)
        self.SecondName.setValidator(QRegExpValidator(CommonResources.only_letter, self.SecondName))
        self.SecondName.setObjectName("SecondName")
        self.SecondName.textEdited.connect(self.SecondNamefirstToUpper)
        self.form.addRow(title, self.SecondName)

        title = QLabel("Пол")
        title.setFont(CommonResources.commonTextFont)

        self.sex = QComboBox()
        self.sex.addItems(CommonResources.getAllVariantsFromCatalog("spr_Sex"))
        self.sex.setFont(CommonResources.commonTextFont)
        self.sex.setObjectName("sex")
        self.sex.setFixedWidth(600)
        self.sex.setCurrentIndex(0)
        self.form.addRow(title, self.sex)

        title = QLabel("Пол")
        title.setFont(CommonResources.commonTextFont)

        self.birthday = QDateTimeEdit()
        curDateTime = QDateTime.currentDateTime()
        self.birthday.setDateTimeRange(curDateTime.addYears(-150), curDateTime.addYears(-18))
        self.birthday.setDateTime(curDateTime.addYears(-18))
        self.form.addRow(title, self.birthday)



        self.has_priveledge = QCheckBox()
        self.has_priveledge.setText("Есть льготы?")
        self.has_priveledge.setObjectName("has_priviledge")
        self.has_priveledge.setFont(CommonResources.commonTextFont)
        self.has_priveledge.stateChanged.connect(self.checkPriviledge)
        self.has_priveledge.setChecked(False)

        title = QLabel("")
        title.setFont(CommonResources.commonTextFont)
        self.form.addRow(self.has_priveledge,title)


        title = QLabel("Льготы")
        title.setFont(CommonResources.commonTextFont)

        self.priviledge = QComboBox()
        self.priviledge.setEnabled(False)
        self.priviledge.setMaximumWidth(600)
        self.priviledge.addItems(CommonResources.getAllVariantsFromCatalog("spr_Priviledge",2))
        self.priviledge.setFont(CommonResources.commonTextFont)
        self.priviledge.setObjectName("priveledge")
        self.priviledge.setCurrentIndex(0)
        self.form.addRow(title, self.priviledge)

        title = QLabel("Занятость")
        title.setFont(CommonResources.commonTextFont)

        self.employment = QComboBox()
        self.employment.addItems(CommonResources.getAllVariantsFromCatalog("spr_Employment"))
        self.employment.setMaximumWidth(600)
        self.employment.setFont(CommonResources.commonTextFont)
        self.employment.setObjectName("employment")
        self.employment.setCurrentIndex(0)
        self.form.addRow(title, self.employment)

        title = QLabel("Место работы")
        title.setFont(CommonResources.commonTextFont)

        self.workplace = QLineEdit()
        self.workplace.setFont(CommonResources.commonTextFont)
        self.workplace.setMaxLength(50)
        self.workplace.setObjectName("workplace")
        self.form.addRow(title, self.workplace)

        title = QLabel("Паспорт")
        title.setFont(CommonResources.commonTextFont)

        self.passport = QPushButton()
        self.passport.setText("Добавить")  # TODO - проверка на наличие
        self.passport.setFont(CommonResources.commonTextFont)
        self.passport.setObjectName("addPassport")
        self.passport.clicked.connect(self.addPassport)
        self.form.addRow(title, self.passport)

        title = QLabel("СНИЛС")
        title.setFont(CommonResources.commonTextFont)

        self.snils = QLineEdit()
        self.snils.setFont(CommonResources.commonTextFont)
        self.snils.setMaxLength(11)#TODO - pretty print
        self.snils.setValidator(QRegExpValidator(CommonResources.snils, self.snils))
        self.snils.setObjectName("snils")
        self.form.addRow(title, self.snils)

        title = QLabel("Полис")
        title.setFont(CommonResources.commonTextFont)

        self.police = QPushButton()
        self.police.setText("Добавить")#TODO - проверка на наличие
        self.police.setFont(CommonResources.commonTextFont)
        self.police.setObjectName("police")
        self.police.clicked.connect(self.addPolice)
        self.form.addRow(title, self.police)

        title = QLabel("Семейное\nположение")
        title.setFont(CommonResources.commonTextFont)

        self.family_status = QComboBox()
        self.family_status.addItems(CommonResources.getAllVariantsFromCatalog("spr_FamilyStatus"))
        self.family_status.setMaximumWidth(600)
        self.family_status.setFont(CommonResources.commonTextFont)
        self.family_status.setCurrentIndex(0)
        self.family_status.setObjectName("family_status")
        self.form.addRow(title, self.family_status)

        title = QLabel("Телефон")
        title.setFont(CommonResources.commonTextFont)

        self.telephone = QLineEdit()
        self.telephone.setFont(CommonResources.commonTextFont)
        self.telephone.setMaxLength(11)  # TODO - pretty print
        self.telephone.setValidator(QRegExpValidator(CommonResources.telephone, self.telephone))
        self.telephone.setObjectName("telephone")
        self.form.addRow(title, self.telephone)

        title = QLabel("Положение")
        title.setFont(CommonResources.commonTextFont)
        title.setVisible(False)

        self.save = QPushButton()
        self.save.setText("Сохранить")
        self.save.setFont(CommonResources.commonTextFont)
        self.save.setObjectName("save")
        self.save.clicked.connect(self.SavingResult)
        self.form.addRow(title, self.save)
        self.form.setSpacing(20)

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
        pass

    def SirnamefirstToUpper(self, text):
        self.Sirname.setText(text.capitalize())

    def NamefirstToUpper(self, text):
        self.Name.setText(text.capitalize())

    def SecondNamefirstToUpper(self, text):
        self.SecondName.setText(text.capitalize())

    def addPassport(self):
        pass

    def addPolice(self):
        pass
