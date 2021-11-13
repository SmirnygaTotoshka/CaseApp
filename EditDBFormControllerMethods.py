from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

import CommonResources


def savePatient(self, action):
    if len(self.Sirname.text()) == 0:
        QMessageBox.warning(self, "Ошибка", "Введите фамилию.", QMessageBox.Ok)
        self.Sirname.setFocus()
        return False
    if len(self.Name.text()) == 0:
        QMessageBox.warning(self, "Ошибка", "Введите имя.", QMessageBox.Ok)
        self.Name.setFocus()
        return False
    if len(self.telephone.text()) < 12:
        QMessageBox.warning(self, "Ошибка", "Введите телефон.", QMessageBox.Ok)
        self.telephone.setFocus()
        return False
    if self.selected_passport is None:
        QMessageBox.warning(self, "Ошибка", "Выберите паспорт.", QMessageBox.Ok)
        self.passport.setFocus()
        return False
    if self.selected_police is None:
        QMessageBox.warning(self, "Ошибка", "Выберите полис.", QMessageBox.Ok)
        self.police.setFocus()
        return False
    if action == CommonResources.ADD:
        query = "INSERT INTO tbl_Patients (Sirname,Name, SecondName, Sex, Birthday, Priviledge, Employment, Workplace," + \
            "PassportID,SnilsID,PoliceID,FamilyStatus,Telephone) VALUES (:Sirname,:Name, :SecondName, :Sex, CAST(:Birthday AS date), :Priviledge, :Employment, :Workplace," + \
            ":PassportID,:SnilsID,:PoliceID,:FamilyStatus,:Telephone)"
    elif action == CommonResources.UPDATE:
        query = "UPDATE tbl_Patients SET Sirname=:Sirname,Name=:Name, SecondName=:SecondName, Sex=:Sex, Birthday=CAST(:Birthday AS date)," +\
                " Priviledge=:Priviledge, Employment=:Employment, Workplace=:Workplace," + \
            "PassportID=:PassportID,SnilsID=:SnilsID,PoliceID=:PoliceID,FamilyStatus=:FamilyStatus,Telephone=:Telephone " + \
            "WHERE ID = :ID"
    add = QSqlQuery()
    if not add.prepare(query):
        QMessageBox.warning(self, "Ошибка", add.lastError().text(), QMessageBox.Ok)
        print(add.lastQuery())
        return False
    if action == CommonResources.UPDATE:
        r = self.parent.tv_Data.selectionModel().selectedRows()[0].row()
        id = self.parent.dataModel.data(self.parent.dataModel.index(r,0))
        add.bindValue(":ID",id)
    add.bindValue(":Sirname", self.Sirname.text())
    add.bindValue(":Name", self.Name.text())
    if self.SecondName.text() == "":
        add.bindValue(":SecondName", None)
    else:
        add.bindValue(":SecondName", self.SecondName.text())
    key = getPrimaryKey(self,"spr_Sex", "NAME", self.sex.itemText(self.sex.currentIndex()))
    if key is not None:
        add.bindValue(":Sex", key[0])

    add.bindValue(":Birthday", self.birthday.date().toString("yyyyMMdd"))

    if self.has_priveledge.isChecked():
        key = getPrimaryKey(self,"spr_Priviledge", "NAME", self.priviledge.itemText(self.priviledge.currentIndex()))
    else:
        key = getPrimaryKey(self, "spr_Priviledge", "NAME", "Нет льгот")
    if key is not None:
        add.bindValue(":Priviledge", key[0])


    key = getPrimaryKey(self,"spr_Employment", "NAME", self.employment.itemText(self.employment.currentIndex()))
    if key is not None:
        add.bindValue(":Employment", key[0])

    if self.SecondName.text() == "":
        add.bindValue(":Workplace", None)
    else:
        add.bindValue(":Workplace", self.workplace.text())

    key = getPrimaryKey(self,"tbl_Passports", "Number", self.selected_passport.getText())
    if key is not None:
        add.bindValue(":PassportID", key[0])

    if self.snils.text() == "":
        add.bindValue(":SnilsID", None)
    else:
        add.bindValue(":SnilsID", self.snils.text())

    key = getPrimaryKey(self,"tbl_Polices","Number", self.selected_police.getText())
    if key is not None:
        add.bindValue(":PoliceID", key[0])

    key = getPrimaryKey(self,"spr_FamilyStatus", "NAME", self.family_status.itemText(self.family_status.currentIndex()))
    if key is not None:
        add.bindValue(":FamilyStatus", key[0])

    add.bindValue(":Telephone", self.telephone.text())
    f = add.exec()
    if f:
        QMessageBox.information(self, self.windowTitle(), "Успешно", QMessageBox.Ok)
        self.parent.dataModel.submitAll()
        self.model.select()
    else:
        QMessageBox.information(self, self.windowTitle(), add.lastError().text(), QMessageBox.Ok)
        self.model.revertAll()
    return f

def saveDoctor(self, action):
    if len(self.Sirname.text()) == 0:
        QMessageBox.warning(self, "Ошибка", "Введите фамилию.", QMessageBox.Ok)
        self.Sirname.setFocus()
        return False
    if len(self.Name.text()) == 0:
        QMessageBox.warning(self, "Ошибка", "Введите имя.", QMessageBox.Ok)
        self.Name.setFocus()
        return False
    if len(self.telephone.text()) < 12:
        QMessageBox.warning(self, "Ошибка", "Введите телефон.", QMessageBox.Ok)
        self.telephone.setFocus()
        return False
    if action == CommonResources.ADD:
        q = "INSERT INTO tbl_Doctors VALUES(:sirname,:name,:secondname,:sex,CAST(:birthday AS date),:pos,:spec,:dep,:tel)"
    else:
        q = "UPDATE tbl_Doctors SET Sirname=:sirname,Name=:name,SecondName=:secondname,Sex=:sex,Birthday=:birthday," +\
            "Position=:pos,Speciality=:spec,Department=:dep,Telephone=:tel WHERE ID = :ID"
    query = QSqlQuery()
    if not query.prepare(q):
        QMessageBox.warning(self, "Ошибка", query.lastError().text(), QMessageBox.Ok)
        print(query.lastQuery())
        return False
    if action == CommonResources.UPDATE:
        r = self.parent.tv_Data.selectionModel().selectedRows()[0].row()
        id = self.parent.dataModel.data(self.parent.dataModel.index(r,0))
        query.bindValue(":ID",id)
    query.bindValue(":sirname", self.Sirname.text())
    query.bindValue(":name", self.Name.text())
    query.bindValue(":secondname", self.SecondName.text())

    key = getPrimaryKey(self,"spr_Sex", "NAME", self.sex.itemText(self.sex.currentIndex()))
    if key is not None:
        query.bindValue(":sex", key[0])

    query.bindValue(":birthday", self.birthday.date().toString("yyyyMMdd"))

    key = getPrimaryKey(self,"spr_Positions", "NAME", self.position.itemText(self.position.currentIndex()))
    if key is not None:
        query.bindValue(":pos", key[0])

    key = getPrimaryKey(self,"spr_Speciality", "NAME", self.speciality.itemText(self.speciality.currentIndex()))
    if key is not None:
        query.bindValue(":spec", key[0])

    key = getPrimaryKey(self,"spr_Departments", "NAME", self.department.itemText(self.department.currentIndex()))
    if key is not None:
        query.bindValue(":dep", key[0])

    query.bindValue(":tel", self.telephone.text())
    f = query.exec()
    if f:
        QMessageBox.information(self, self.windowTitle(), "Успешно", QMessageBox.Ok)
        self.model.submitAll()
        self.model.select()
    else:
        QMessageBox.information(self, self.windowTitle(), query.lastError().text(), QMessageBox.Ok)
        self.model.revertAll()
    return f


def saveCase(self, action):
    if self.selected_patient is None:
        QMessageBox.warning(self, "Ошибка", "Выберите пациента.", QMessageBox.Ok)
        self.patient.setFocus()
        return False
    rowCount = self.model.rowCount()
    self.model.insertRows(rowCount, 1)
    self.model.setData(self.model.index(rowCount, 1), int(self.selected_patient.getText().split(" ")[0]))

    key = getPrimaryKey(self, "spr_AidType", "NAME", self.aid_type.itemText(self.aid_type.currentIndex()))
    if key is not None:
        self.model.setData(self.model.index(rowCount, 2), key[0])

    key = getPrimaryKey(self, "spr_Purpose", "NAME", self.purpose.itemText(self.purpose.currentIndex()))
    if key is not None:
        self.model.setData(self.model.index(rowCount, 3), key[0])

    key = getPrimaryKey(self, "spr_Result", "NAME", self.result.itemText(self.result.currentIndex()))
    if key is not None:
        self.model.setData(self.model.index(rowCount, 4), key[0])

    key = getPrimaryKey(self, "spr_MKB", "MKB_NAME", self.mkb.itemText(self.mkb.currentIndex()))
    if key is not None:
        self.model.setData(self.model.index(rowCount, 5), key[0])

    key = getPrimaryKey(self, "spr_DiseaseType", "NAME", self.disease_type.itemText(self.disease_type.currentIndex()))
    if key is not None:
        self.model.setData(self.model.index(rowCount, 6), key[0])

    f = self.model.submitAll()
    if f:
        QMessageBox.information(self, self.windowTitle(), "Успешно", QMessageBox.Ok)
        self.model.select()
    else:
        QMessageBox.warning(self, self.windowTitle(), "Запись не добавлена\n" + self.model.lastError().text(),
                            QMessageBox.Ok)
        self.model.revertAll()
    return f


def saveVisit(self, action):
    if self.selected_doctor is None:
        QMessageBox.warning(self, "Ошибка", "Выберите врача.", QMessageBox.Ok)
        self.doctor.setFocus()
        return False
    if self.selected_case is None:
        QMessageBox.warning(self, "Ошибка", "Выберите случай.", QMessageBox.Ok)
        self.case.setFocus()
        return False
    q = "INSERT INTO tbl_Visit VALUES(:doctorID,:caseID,CAST(:d AS date),:place,:circ)"
    query = QSqlQuery()
    if not query.prepare(q):
        QMessageBox.warning(self, "Ошибка", query.lastError().text(), QMessageBox.Ok)
        print(query.lastQuery())
        return False
    query.bindValue(":doctorID", int(self.selected_doctor.getText().split(" ")[0]))
    query.bindValue(":caseID", int(self.selected_case.getText()))
    query.bindValue(":d", self.date.date().toString("yyyyMMdd"))

    key = getPrimaryKey(self, "spr_VisitPlace", "NAME", self.visit_place.itemText(self.visit_place.currentIndex()))
    if key is not None:
        query.bindValue(":place", key[0])

    key = getPrimaryKey(self, "spr_VisitCircumstances", "NAME", self.visit_circumstances.itemText(self.visit_circumstances.currentIndex()))
    if key is not None:
        query.bindValue(":circ", key[0])

    f = query.exec()
    if f:
        QMessageBox.information(self, self.windowTitle(), "Успешно", QMessageBox.Ok)
        self.model.submitAll()
        self.model.select()
    else:
        QMessageBox.information(self, self.windowTitle(), query.lastError().text(), QMessageBox.Ok)
        self.model.revertAll()
    return f


def saveServices(self, action):
    if self.selected_visit is None:
        QMessageBox.warning(self, "Ошибка", "Выберите посещение.", QMessageBox.Ok)
        self.visit.setFocus()
        return False
    rowCount = self.model.rowCount()
    self.model.insertRows(rowCount, 1)
    self.model.setData(self.model.index(rowCount, 1), int(self.selected_visit.getText()))

    key = getPrimaryKey(self, "spr_CodeServices", "NAME", self.service.itemText(self.service.currentIndex()))
    if key is not None:
        self.model.setData(self.model.index(rowCount, 2), key[0])

    key = getPrimaryKey(self, "spr_PaymentType", "FULL_NAME", self.payment_type.itemText(self.payment_type.currentIndex()))
    if key is not None:
        self.model.setData(self.model.index(rowCount, 3), key[0])

    f = self.model.submitAll()
    if f:
        QMessageBox.information(self, self.windowTitle(), "Успешно", QMessageBox.Ok)
        self.model.select()
    else:
        QMessageBox.warning(self, self.windowTitle(), "Запись не добавлена\n" + self.model.lastError().text(),
                            QMessageBox.Ok)
        self.model.revertAll()
    return f


def savePassports(self, action):
    q = QMessageBox.Yes
    if len(self.number.text()) != 11:
        QMessageBox.warning(self, "Ошибка", "Введите корректную серию и номер паспорта.", QMessageBox.Ok)
        return False
    if len(self.address.text()) < 15:
        q = QMessageBox.warning(self, "Ошибка", "Возможно некорректный адрес. Продолжить?",
                                QMessageBox.Yes | QMessageBox.No)
    if q == QMessageBox.Yes or len(self.address.text()) >= 15:
        rowCount = self.model.rowCount()
        self.model.insertRows(rowCount, 1)
        self.model.setData(self.model.index(rowCount, 1), self.number.text().replace(" ", ""))
        self.model.setData(self.model.index(rowCount, 2), self.address.text())
        f = self.model.submitAll()
        if f:
            QMessageBox.information(self, self.windowTitle(), "Успешно", QMessageBox.Ok)
            self.model.select()
        else:
            QMessageBox.information(self, self.windowTitle(), self.model.lastError().text(), QMessageBox.Ok)
            self.model.revertAll()
        return f
    else:
        return False


def savePolices(self, action):
    if len(self.police_number.text()) != 16:
        QMessageBox.warning(self, "Ошибка", "Введите корректный номер полиса.", QMessageBox.Ok)
        return False
    rowCount = self.model.rowCount()
    self.model.insertRows(rowCount, 1)
    self.model.setData(self.model.index(rowCount, 1), self.police_number.text())
    key = getPrimaryKey(self,"spr_SMO", "NAM_SMOP", self.smo.itemText(self.smo.currentIndex()))
    if key is not None:
        self.model.setData(self.model.index(rowCount, 2), key[0])
        f = self.model.submitAll()
    else:
        f = False
    if f:
        QMessageBox.information(self, self.windowTitle(), "Успешно", QMessageBox.Ok)
        self.model.select()
    else:
        QMessageBox.warning(self, self.windowTitle(), "Запись не добавлена\n" + self.model.lastError().text(),
                            QMessageBox.Ok)
        self.model.revertAll()
    return f


def getPrimaryKey(self, table, column, value):
    qsql = QSqlQuery()
    query = "select ID from " + table + " where " + column + " = :val;"
    q = qsql.prepare(query)
    if not q:
        QMessageBox.information(self, self.windowTitle(), "Query not prepared, because\n" + qsql.lastError().text(),
                                QMessageBox.Ok)
        return None
    qsql.bindValue(":val", value)
    q = qsql.exec_()
    if not q:
        QMessageBox.information(self, self.windowTitle(), "Query not executed, because\n" + qsql.lastError().text(),
                                QMessageBox.Ok)
        return None
    values = []
    while (qsql.next()):
        values.append(qsql.value(0))
    return values