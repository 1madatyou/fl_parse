from typing import List, Type

from PyQt5 import QtCore, QtGui, QtWidgets

from base.services import BaseFreelanceService
from write import XLSXWriter, JsonWriter


class FLGUI():

    def __init__(self, fl_services: List[Type[BaseFreelanceService]]) -> None:
        self.fl_services = {service.PLATFORM: service() for service in fl_services}

    def _init_service_combo_box(self):
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems([service_platform for service_platform in self.fl_services])
        self.current_service = self.fl_services[self.comboBox.currentText()]

    def _init_service_category_checkboxes(self):
        self.checkboxes = []
        counter = 0
        for category in self.current_service.get_categories():
            new_checkbox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
            new_checkbox.setText(category.name)
            self.verticalLayout_4.addWidget(new_checkbox)
            self.checkboxes.append(new_checkbox)
            counter += 1
            if counter == 200:
                break
    
    def _init_start_button(self):
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 440, 261, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.start)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(381, 553)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self._init_start_button()

        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 370, 71, 52))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.formLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.JsonCheckbox = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.XlsxCheckbox = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.verticalLayout.addWidget(self.JsonCheckbox)
        self.verticalLayout.addWidget(self.XlsxCheckbox)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 341, 56))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self._init_service_combo_box()
        self.verticalLayout_2.addWidget(self.comboBox)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 100, 341, 201))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)

        self.selectAllCheckbox = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.selectAllCheckbox.setObjectName("selectAllCheckbox")
        self.verticalLayout_3.addWidget(self.selectAllCheckbox)
        self.selectAllCheckbox.stateChanged.connect(self._change_all_checkboxes_state)

        self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget_2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 337, 147))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self._init_service_category_checkboxes()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        self.verticalLayout_3.addWidget(self.scrollArea)

        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(20, 310, 160, 51))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)

        self.countOfOrdersInput = QtWidgets.QTextEdit(self.verticalLayoutWidget_4)
        self.countOfOrdersInput.setObjectName("textEdit")

        self.verticalLayout_6.addWidget(self.countOfOrdersInput)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 381, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _change_all_checkboxes_state(self, state):
        for checkbox in self.checkboxes:
            checkbox.setChecked(state)

    def start(self):
        service = self.current_service
        writing_methods = []
        if self.XlsxCheckbox.isChecked():
            writing_methods.append(XLSXWriter)
        if self.JsonCheckbox.isChecked():
            writing_methods.append(JsonWriter)
        service.set_writing_methods(writing_methods)
        count_of_orders = int(self.countOfOrdersInput.toPlainText())
        category_names = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        service.execute(category_names, count_of_orders)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.XlsxCheckbox.setText(_translate("MainWindow", ".XLSX"))
        self.JsonCheckbox.setText(_translate("MainWindow", ".JSON"))
        self.label.setText(_translate("MainWindow", "Service:"))
        self.label_2.setText(_translate("MainWindow", "Categories:"))
        self.selectAllCheckbox.setText(_translate("MainWindow", "Select all"))
        self.label_3.setText(_translate("MainWindow", "Count of orders:"))

