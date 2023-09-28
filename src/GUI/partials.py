from PyQt5 import QtGui, QtWidgets



class CustomProgressDialog(QtWidgets.QProgressDialog):

    def __init__(self, parent):
        super().__init__('Executing...', 'Close', 0, 100, parent)
        self.setRange(0, 0)
        self.setCancelButton(None)
        self.setAutoClose(False)
        self.setAutoReset(False)
        self.close()

    
    def closeEvent(self, event) -> None:
        self.setLabelText('Executing...')
        return super().closeEvent(event)
    