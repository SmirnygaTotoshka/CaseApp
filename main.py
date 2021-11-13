# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from PyQt5 import QtWidgets
import CommonResources
from forms import frm_MainWindow


def init_res(app):
    CommonResources.screen = app.primaryScreen()
    CommonResources.screen_width = CommonResources.screen.availableGeometry().width()
    CommonResources.screen_height = CommonResources.screen.availableGeometry().height()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if CommonResources.database.open():
        app = QtWidgets.QApplication(sys.argv)
        init_res(app)
        window = frm_MainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        print("Unable to open data source file.")
        sys.exit(1)  # Error code 1 - signifies error
    #app = QtWidgets.QApplication(sys.argv)
    #window = Ui_MainWindow()
    #window.setupUI(window)
    #window.show()
    #sys.exit(app.exec_())
#     import pyodbc
#
#     # Some other example server values are
#     # server = 'localhost\sqlexpress' # for a named instance
#     # server = 'myserver,port' # to specify an alternate port
#     server = 'SMIRNYGATOTOSHK\SQLEXPRESS'
#     database = 'ambulatoryCase'
#     username = 'SMIRNYGATOTOSHK\SmirnygaTotoshka'
#     conn = pyodbc.connect('Driver={SQL Server};'
#                           'Server=SMIRNYGATOTOSHK\SQLEXPRESS;'
#                           'Database=ambulatoryCase;'
#                           'Trusted_Connection=yes;')
#     cursor = conn.cursor()
#     print(cursor)
#     print_hi('PyCharm')
#
#     cursor.execute('SELECT * FROM spr_Sex')
#
#     for i in cursor:
#         print(i)
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
