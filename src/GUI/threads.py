from typing import List
from PyQt5.QtCore import QObject, QThread

from base.services import BaseFreelanceService


class ExecutingThread(QThread):

    def __init__(
        self,
        parent: QObject | None,
        gui,
        service: BaseFreelanceService,
        category_names: List[str],
        count_of_orders: int,
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.gui = gui
        self.service = service
        self.category_names = category_names
        self.count_of_orders = count_of_orders

    def run(self):
        self.service.execute(self.category_names, self.count_of_orders)
        self.gui.progressDialog.setValue(100)
        self.gui.progressDialog.setLabelText("Completed successfully")
