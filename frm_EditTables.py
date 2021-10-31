from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime
from PyQt5.QtSql import QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTableWidgetItem, \
    QDateTimeEdit, QMessageBox, QAbstractItemView, QAction, QHeaderView
from PyQt5.QtCore import Qt
import CommonResources


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.commonSetup()
        self.setupTabWidget()

    def commonSetup(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("Учёт амбулаторных посещений (учебная версия)")
        self.setMinimumSize(640, 480)
        self.setMaximumSize(16777215, 16777215)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.globalLayout = QGridLayout(self.centralwidget)
        self.setupFonts()
        self.setupTabWidget()
        self.globalLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralwidget)



    def setupFonts(self):
        self.commonTextFont = QtGui.QFont()
        self.commonTextFont.setFamily("Times New Roman")
        self.commonTextFont.setPointSize(14)

    def setupTabWidget(self):
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, CommonResources.screen_width, CommonResources.screen_height))
        #TODO - write meaning all Polices
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setFont(self.commonTextFont)
        self.tabWidget.setObjectName("tabWidget")

        self.globalLayout = QVBoxLayout(self.centralwidget)
        self.globalLayout.setContentsMargins(10, 20, 10, 50)
        self.globalLayout.setStretch(0, 0)
        self.globalLayout.addWidget(self.tabWidget)
        self.createCheckReferences()
        #self.createPatientsTab()
        self.tabWidget.addTab(self.tab_checkReferences,"")
        #self.tabWidget
        self.tabWidget.setTabText(0,"Проверить справочники")
        self.tabWidget.setCurrentIndex(0)

    def createCheckReferences(self):
        self.tab_checkReferences = QtWidgets.QWidget()
        self.tab_checkReferences.setObjectName("checkReferences")

        self.tv_checkReferences = QtWidgets.QTableView(self.tab_checkReferences)
        #self.tv_checkReferences.setGeometry(QtCore.QRect(100, 200, 1200, 391))
        self.tv_checkReferences.setObjectName("tw_checkReferences")
        sizePolicyTable = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicyTable.setHeightForWidth(self.tv_checkReferences.sizePolicy().hasHeightForWidth())
        self.tv_checkReferences.setSizePolicy(sizePolicyTable)

        self.catalog_type = QComboBox()
        names = self.getTableNames("spr_")
        self.catalog_type.addItems(names)
        #self.catalog_type.move(200, 200)
        #self.catalog_type.currentIndexChanged.connect(self.onEventTypeChanged)
        self.catalog_type.setCurrentIndex(0)

        self.catalogModel = QSqlTableModel()
        self.catalogModel.setTable(names[0])
        self.tv_checkReferences.setModel(self.catalogModel)
        self.tv_checkReferences.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tv_checkReferences.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tv_checkReferences.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv_checkReferences.horizontalHeader().setCascadingSectionResizes(True)
        self.tv_checkReferences.horizontalHeader().setDefaultSectionSize(200)
        self.tv_checkReferences.horizontalHeader().setMinimumSectionSize(100)
        self.tv_checkReferences.horizontalHeader().setSortIndicatorShown(True)
        self.tv_checkReferences.horizontalHeader().setStretchLastSection(True)
        self.tv_checkReferences.verticalHeader().setStretchLastSection(False)
        self.catalog_type.currentIndexChanged.connect(self.onCatalogChanged)
        self.catalogModel.select()

        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(10, 20, 10, 50)
        vLayout.setStretch(0, 0)
        vLayout.addWidget(self.catalog_type)
        vLayout.addWidget(self.tv_checkReferences)
        self.tab_checkReferences.setLayout(vLayout)

    def createTab(self,index, title, QWidget) -> QTableWidgetItem:
        pass

    def onCatalogChanged(self,index):
        names = self.getTableNames("spr_")
        self.catalogModel.setTable(names[index])
        self.catalogModel.select()

    def getTableNames(self,name:str) -> list:
        names = []
        for n in CommonResources.database.tables():
            if name in n:
                names.append(n)
        return names
        # table_names = QSqlQuery()
        # table_names.prepare("SELECT TABLE_NAME FROM ambulatoryCase.INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE ?")
        # if prefix:
        #     name += "%"
        # table_names.addBindValue(name)
        # table_names.exec_()
        # names = []
        # while (table_names.next()):
        #     s = table_names.value(0)
        #     names.append(s)
        # return names