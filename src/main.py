from typing import List, Type
import sys

from PyQt5 import QtWidgets

from base.services import BaseFreelanceService
from utils import measure_time
from freelance_services.weblancer.service import WeblancerService
from GUI.main import FLGUI


if __name__ == '__main__':
    service_list = [
        WeblancerService
    ]
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = FLGUI(service_list)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())