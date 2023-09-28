import sys

from PyQt5 import QtWidgets

from freelance_services.weblancer.service import WeblancerService
from freelance_services.freelanceRU.service import FreelanceRUService
from GUI.main import MainGUI


if __name__ == '__main__':
    service_list = [
        WeblancerService,
        FreelanceRUService
    ]
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainGUI(service_list)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    # for i in FreelanceRUService().categories:
    #     print(i.name)
    #     print(i.href)