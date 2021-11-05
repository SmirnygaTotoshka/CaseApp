
import sys

from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

if __name__ == '__main__':
    database = QSqlDatabase.addDatabase("QODBC")
    database.setDatabaseName('Driver={SQL Server};'
                             'Server=SMIRNYGATOTOSHK\SQLEXPRESS;'
                             'Database=ambulatoryCase;'
                             'Trusted_Connection=yes;')
    if database.open():
        print("Success")
        try:
            table_names = QSqlQuery()
            query = "select ID from spr_SMO where NAM_SMOP = :val;"
            q = table_names.prepare(query)
            if not q:
                print(table_names.lastError().text())
            #table_names.bindValue(":id","ID")
            table_names.bindValue(":col","NAM_SMOP")
            #table_names.addBindValue("NAM_SMOP")
            table_names.bindValue(":val","ФИЛИАЛ АКЦИОНЕРНОГО ОБЩЕСТВА \"МЕДИЦИНСКАЯ АКЦИОНЕРНАЯ СТРАХОВАЯ КОМПАНИЯ\" В ГОРОДЕ УФЕ")
            #table_names.addBindValue("spr_Sex")
            q = table_names.exec_()
            if not q:
                print(table_names.lastError().text())
            values = []
            while (table_names.next()):
                values.append(table_names.value(0))
            print(values)
            print(table_names.lastQuery())
            print(table_names.boundValues())
            print(table_names.lastError().text())
            print(table_names.executedQuery())
        except Exception as e:
            print(e)
    else:
        sys.exit(1)