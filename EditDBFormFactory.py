from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QDateEdit, QComboBox, QCheckBox

import CommonResources


def createPatientForm(self, action):
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

    title = QLabel("Дата рождения")
    title.setFont(CommonResources.commonTextFont)

    self.birthday = QDateEdit()
    curDateTime = self.birthday.date().currentDate()
    self.birthday.setDateRange(curDateTime.addYears(-150), curDateTime.addYears(-18))
    self.birthday.setDate(curDateTime.addYears(-18))
    self.birthday.setObjectName("birthday")
    self.birthday.setCalendarPopup(True)
    self.form.addRow(title, self.birthday)

    self.has_priveledge = QCheckBox()
    self.has_priveledge.setText("Есть льготы?")
    self.has_priveledge.setObjectName("has_priviledge")
    self.has_priveledge.setFont(CommonResources.commonTextFont)
    self.has_priveledge.stateChanged.connect(self.checkPriviledge)
    self.has_priveledge.setChecked(False)

    title = QLabel("")
    title.setFont(CommonResources.commonTextFont)
    self.form.addRow(self.has_priveledge, title)

    title = QLabel("Льготы")
    title.setFont(CommonResources.commonTextFont)

    self.priviledge = QComboBox()
    self.priviledge.setEnabled(False)
    self.priviledge.setMaximumWidth(500)
    self.priviledge.addItems(CommonResources.getAllVariantsFromCatalog("spr_Priviledge", 2))
    self.priviledge.setFont(CommonResources.commonTextFont)
    self.priviledge.setObjectName("priveledge")
    self.priviledge.setCurrentIndex(0)
    self.form.addRow(title, self.priviledge)

    title = QLabel("Занятость")
    title.setFont(CommonResources.commonTextFont)

    self.employment = QComboBox()
    self.employment.addItems(CommonResources.getAllVariantsFromCatalog("spr_Employment"))
    self.employment.setMaximumWidth(500)
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

    self.selected_passport = None

    title = QLabel("СНИЛС")
    title.setFont(CommonResources.commonTextFont)

    self.snils = QLineEdit()
    self.snils.setFont(CommonResources.commonTextFont)
    self.snils.setMaxLength(11)  # TODO - pretty print
    self.snils.setValidator(QRegExpValidator(CommonResources.snils, self.snils))
    self.snils.setObjectName("snils")
    self.form.addRow(title, self.snils)

    title = QLabel("Полис")
    title.setFont(CommonResources.commonTextFont)

    self.police = QPushButton()
    self.police.setText("Добавить")  # TODO - проверка на наличие
    self.police.setFont(CommonResources.commonTextFont)
    self.police.setObjectName("police")
    self.police.clicked.connect(self.addPolice)
    self.form.addRow(title, self.police)

    self.selected_police = None

    title = QLabel("Семейное\nположение")
    title.setFont(CommonResources.commonTextFont)

    self.family_status = QComboBox()
    self.family_status.addItems(CommonResources.getAllVariantsFromCatalog("spr_FamilyStatus"))
    self.family_status.setMaximumWidth(500)
    self.family_status.setFont(CommonResources.commonTextFont)
    self.family_status.setCurrentIndex(0)
    self.family_status.setObjectName("family_status")
    self.form.addRow(title, self.family_status)

    title = QLabel("Телефон")
    title.setFont(CommonResources.commonTextFont)

    self.telephone = QLineEdit()
    self.telephone.setFont(CommonResources.commonTextFont)
    self.telephone.setMaxLength(12)  # TODO - pretty print
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


def createDoctorForm(self, action):
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
    self.sex.setFixedWidth(500)
    self.sex.setCurrentIndex(0)
    self.form.addRow(title, self.sex)

    title = QLabel("Дата рождения")
    title.setFont(CommonResources.commonTextFont)

    self.birthday = QDateEdit()
    curDateTime = self.birthday.date().currentDate()
    self.birthday.setDateRange(curDateTime.addYears(-150), curDateTime.addYears(-18))
    self.birthday.setDate(curDateTime.addYears(-18))
    self.birthday.setObjectName("birthday")
    self.birthday.setCalendarPopup(True)
    self.form.addRow(title, self.birthday)

    title = QLabel("Должность")
    title.setFont(CommonResources.commonTextFont)

    self.position = QComboBox()
    self.position.addItems(CommonResources.getAllVariantsFromCatalog("spr_Positions"))
    self.position.setMaximumWidth(500)
    self.position.setFont(CommonResources.commonTextFont)
    self.position.setCurrentIndex(0)
    self.position.setObjectName("position")
    self.form.addRow(title, self.position)

    title = QLabel("Специальность")
    title.setFont(CommonResources.commonTextFont)

    self.speciality = QComboBox()
    self.speciality.addItems(CommonResources.getAllVariantsFromCatalog("spr_Speciality"))
    self.speciality.setMaximumWidth(500)
    self.speciality.setFont(CommonResources.commonTextFont)
    self.speciality.setCurrentIndex(0)
    self.speciality.setObjectName("speciality")
    self.form.addRow(title, self.speciality)

    title = QLabel("Отделение")
    title.setFont(CommonResources.commonTextFont)

    self.department = QComboBox()
    self.department.addItems(CommonResources.getAllVariantsFromCatalog("spr_Departments"))
    self.department.setMaximumWidth(500)
    self.department.setFont(CommonResources.commonTextFont)
    self.department.setCurrentIndex(0)
    self.department.setObjectName("department")
    self.form.addRow(title, self.department)

    title = QLabel("Телефон")
    title.setFont(CommonResources.commonTextFont)

    self.telephone = QLineEdit()
    self.telephone.setFont(CommonResources.commonTextFont)
    self.telephone.setMaxLength(12)  # TODO - pretty print
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


def createCaseForm(self, action):
    title = QLabel("Пациент")
    title.setFont(CommonResources.commonTextFont)

    self.patient = QPushButton()
    self.patient.setText("Выбрать")  # TODO - проверка на наличие
    self.patient.setFont(CommonResources.commonTextFont)
    self.patient.setObjectName("patient")
    self.patient.clicked.connect(self.selectPatient)
    self.form.addRow(title, self.patient)

    title = QLabel("Тип помощи")
    title.setFont(CommonResources.commonTextFont)

    self.aid_type = QComboBox()
    self.aid_type.addItems(CommonResources.getAllVariantsFromCatalog("spr_AidType"))
    self.aid_type.setMaximumWidth(600)
    self.aid_type.setFont(CommonResources.commonTextFont)
    self.aid_type.setCurrentIndex(0)
    self.aid_type.setObjectName("aid_type")
    self.form.addRow(title, self.aid_type)

    title = QLabel("Цель")
    title.setFont(CommonResources.commonTextFont)

    self.purpose = QComboBox()
    self.purpose.addItems(CommonResources.getAllVariantsFromCatalog("spr_Purpose"))
    self.purpose.setMaximumWidth(600)
    self.purpose.setFont(CommonResources.commonTextFont)
    self.purpose.setCurrentIndex(0)
    self.purpose.setObjectName("purpose")
    self.form.addRow(title, self.purpose)

    title = QLabel("Результат")
    title.setFont(CommonResources.commonTextFont)

    self.result = QComboBox()
    self.result.addItems(CommonResources.getAllVariantsFromCatalog("spr_Result"))
    self.result.setMaximumWidth(600)
    self.result.setFont(CommonResources.commonTextFont)
    self.result.setCurrentIndex(0)
    self.result.setObjectName("result")
    self.form.addRow(title, self.result)

    title = QLabel("Диагноз")
    title.setFont(CommonResources.commonTextFont)

    self.mkb = QComboBox()
    self.mkb.addItems(CommonResources.getAllVariantsFromCatalog("spr_MKB", 2))
    self.mkb.setMaximumWidth(600)
    self.mkb.setFont(CommonResources.commonTextFont)
    self.mkb.setCurrentIndex(0)
    self.mkb.setObjectName("mkb")
    self.form.addRow(title, self.mkb)

    title = QLabel("Тип заболевания")
    title.setFont(CommonResources.commonTextFont)

    self.disease_type = QComboBox()
    self.disease_type.addItems(CommonResources.getAllVariantsFromCatalog("spr_DiseaseType"))
    self.disease_type.setMaximumWidth(600)
    self.disease_type.setFont(CommonResources.commonTextFont)
    self.disease_type.setCurrentIndex(0)
    self.disease_type.setObjectName("disease_type")
    self.form.addRow(title, self.disease_type)

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

def createVisitForm(self,action):
    title = QLabel("Доктор")
    title.setFont(CommonResources.commonTextFont)

    self.doctor = QPushButton()
    self.doctor.setText("Выбрать")  # TODO - проверка на наличие
    self.doctor.setFont(CommonResources.commonTextFont)
    self.doctor.setObjectName("doctor")
    self.doctor.clicked.connect(self.selectDoctor)
    self.form.addRow(title, self.doctor)

    title = QLabel("Случай")
    title.setFont(CommonResources.commonTextFont)

    self.case = QPushButton()
    self.case.setText("Выбрать")  # TODO - проверка на наличие
    self.case.setFont(CommonResources.commonTextFont)
    self.case.setObjectName("case")
    self.case.clicked.connect(self.selectCase)
    self.form.addRow(title, self.case)

    title = QLabel("Дата посещения")
    title.setFont(CommonResources.commonTextFont)

    self.date = QDateEdit()
    curDateTime = self.date.date().currentDate()
    self.date.setDateRange(curDateTime.addYears(-150), curDateTime)
    self.date.setDate(curDateTime)
    self.date.setObjectName("date")
    self.date.setCalendarPopup(True)
    self.form.addRow(title, self.date)

    title = QLabel("Место посещения")
    title.setFont(CommonResources.commonTextFont)

    self.visit_place = QComboBox()
    self.visit_place.addItems(CommonResources.getAllVariantsFromCatalog("spr_VisitPlace"))
    self.visit_place.setMaximumWidth(500)
    self.visit_place.setFont(CommonResources.commonTextFont)
    self.visit_place.setCurrentIndex(0)
    self.visit_place.setObjectName("visit_place")
    self.form.addRow(title, self.visit_place)

    title = QLabel("Обстоятельства\n посещения")
    title.setFont(CommonResources.commonTextFont)

    self.visit_circumstances = QComboBox()
    self.visit_circumstances.addItems(CommonResources.getAllVariantsFromCatalog("spr_VisitCircumstances"))
    self.visit_circumstances.setMaximumWidth(500)
    self.visit_circumstances.setFont(CommonResources.commonTextFont)
    self.visit_circumstances.setCurrentIndex(0)
    self.visit_circumstances.setObjectName("visit_circumstances")
    self.form.addRow(title, self.visit_circumstances)

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

def createServicesForm(self,action):
    title = QLabel("Посещение")
    title.setFont(CommonResources.commonTextFont)

    self.visit = QPushButton()
    self.visit.setText("Выбрать")  # TODO - проверка на наличие
    self.visit.setFont(CommonResources.commonTextFont)
    self.visit.setObjectName("visit")
    self.visit.clicked.connect(self.selectVisit)
    self.form.addRow(title, self.visit)

    title = QLabel("Услуга")
    title.setFont(CommonResources.commonTextFont)

    self.service = QComboBox()
    self.service.addItems(CommonResources.getAllVariantsFromCatalog("spr_CodeServices"))
    self.service.setMaximumWidth(500)
    self.service.setFont(CommonResources.commonTextFont)
    self.service.setCurrentIndex(0)
    self.service.setObjectName("service")
    self.form.addRow(title, self.service)

    title = QLabel("Тип оплаты")
    title.setFont(CommonResources.commonTextFont)

    self.payment_type = QComboBox()
    self.payment_type.addItems(CommonResources.getAllVariantsFromCatalog("spr_PaymentType"))
    self.payment_type.setMaximumWidth(500)
    self.payment_type.setFont(CommonResources.commonTextFont)
    self.payment_type.setCurrentIndex(0)
    self.payment_type.setObjectName("payment_type")
    self.form.addRow(title, self.payment_type)

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

def createPassportForm(self, action):
    title = QLabel("Серия и номер")
    title.setFont(CommonResources.commonTextFont)

    self.number = QLineEdit()
    self.number.setFont(CommonResources.commonTextFont)
    self.number.setMaxLength(11)  # TODO - pretty print
    self.number.setValidator(QRegExpValidator(CommonResources.passport_number, self.number))
    self.number.textChanged.connect(self.prettyPassportPrint)
    self.number.setObjectName("number")
    self.form.addRow(title, self.number)

    title = QLabel("Адрес")
    title.setFont(CommonResources.commonTextFont)

    self.address = QLineEdit()
    self.address.setFont(CommonResources.commonTextFont)
    self.address.setValidator(QRegExpValidator(CommonResources.address, self.address))
    self.address.setMaxLength(70)  # TODO - pretty print
    self.address.setObjectName("address")
    self.form.addRow(title, self.address)

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

def createPoliceForm(self,action):
    title = QLabel("Номер")
    title.setFont(CommonResources.commonTextFont)

    self.police_number = QLineEdit()
    self.police_number.setFont(CommonResources.commonTextFont)
    self.police_number.setMaxLength(16)  # TODO - pretty print
    self.police_number.setValidator(QRegExpValidator(CommonResources.police_number, self.police_number))
    self.police_number.setObjectName("police_number")
    self.form.addRow(title, self.police_number)

    title = QLabel("СМО")
    title.setFont(CommonResources.commonTextFont)

    self.smo = QComboBox()
    self.smo.addItems(CommonResources.getAllVariantsFromCatalog("spr_SMO"))
    self.smo.setMaximumWidth(500)
    self.smo.setFont(CommonResources.commonTextFont)
    self.smo.setCurrentIndex(0)
    self.smo.setObjectName("smo")
    self.form.addRow(title, self.smo)

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