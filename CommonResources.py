from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QApplication

database = QSqlDatabase.addDatabase("QODBC")
database.setDatabaseName('Driver={SQL Server};'
                         'Server=SMIRNYGATOTOSHK\SQLEXPRESS;'
                         'Database=ambulatoryCase;'
                         'Trusted_Connection=yes;')
screen = None
screen_width = 0
screen_height = 0

