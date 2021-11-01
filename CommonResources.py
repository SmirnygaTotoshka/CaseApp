from PyQt5 import QtGui
from PyQt5.QtCore import QRegExp
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

database = QSqlDatabase.addDatabase("QODBC")
database.setDatabaseName('Driver={SQL Server};'
                         'Server=SMIRNYGATOTOSHK\SQLEXPRESS;'
                         'Database=ambulatoryCase;'
                         'Trusted_Connection=yes;')
screen = None
screen_width = 0
screen_height = 0

commonTextFont = QtGui.QFont()
commonTextFont.setFamily("Times New Roman")
commonTextFont.setPointSize(14)

only_letter = QRegExp("^[А-Яа-я]{1,50}$")
snils = QRegExp("^[0-9]{11}$")
telephone = QRegExp("(^8|7|\+7)((\d{10})|(\s\(\d{3}\)\s\d{3}\s\d{2}\s\d{2}))")

def getAllVariantsFromCatalog(catalog,col_index = 1) -> list:
    table_names = QSqlQuery()
    query = "SELECT * FROM "+catalog + ";"
    table_names.exec_(query)
    values = []
    while (table_names.next()):
        values.append(table_names.value(col_index))
    return values