
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
            name = "spr_Sex"
            query = "SELECT * FROM "+name + ";"
            table_names.prepare(query)
            #table_names.addBindValue("spr_Sex")
            table_names.exec_()
            values = []
            while (table_names.next()):
                values.append(table_names.value(1))
            print(values)
        except Exception as e:
            print(e)
    else:
        sys.exit(1)