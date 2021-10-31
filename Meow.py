
import sys

from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

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
            # table_names.addBindValue("spr_")
            name = "tbl_Patients"
            table_names.prepare("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?")
            table_names.addBindValue(name)
            table_names.exec_()
            while (table_names.next()):
                print(table_names.value(0))
        except Exception as e:
            print(e)
    else:
        sys.exit(1)