import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication


from freelance_services.weblancer.service import WeblancerService
from freelance_services.freelanceRU.service import FreelanceRUService
from GUI.gui import MainGUI


if __name__ == "__main__":
    service_list = [WeblancerService, FreelanceRUService]

    app = QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainGUI(service_list)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
