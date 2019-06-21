import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication
import bgimgw

class groundstat(QMainWindow):
    def __init__(self):
        super(groundstat, self).__init__()
        loadUi('groundstation.ui', self)

        self.pushButton_20.clicked.connect(self.submit)
        self.pushButton_21.clicked.connect(self.postprocessing)
        self.pushButton_22.clicked.connect(self.realtimeprocessing)
        self.pushButton_23.clicked.connect(self.startserver)
        self.pushButton.clicked.connect(self.connectdrone1)
        self.pushButton_2.clicked.connect(self.connectdrone2)
        self.pushButton_4.clicked.connect(self.openmp1)
        self.pushButton_5.clicked.connect(self.openmp2)
        self.pushButton_18.clicked.connect(self.triangulate)
        self.pushButton_19.clicked.connect(self.display)
        self.pushButton_8.clicked.connect(self.storedata)
        self.pushButton_7.clicked.connect(self.fpv1)
        self.pushButton_9.clicked.connect(self.fpv2)
        self.pushButton_10.clicked.connect(self.close)
        self.message = ""


        #Initialization of line edit
        self.lineEdit = 0.0
        self.lineEdit_10 = 0.0
        self.lineEdit_11 = 0.0
        self.lineEdit_12 = 0.0
        self.lineEdit_13 = 0.0
        self.lineEdit_14 = 0.0
        self.lineEdit_15 = 0.0
        self.lineEdit_16 = 0.0
        self.lineEdit_17 = 0.0
        self.lineEdit_18 = 0.0
        self.lineEdit_2 = 0.0
        self.lineEdit_20 = 0.0
        self.lineEdit_21 = 0.0
        self.lineEdit_24 = 0.0
        self.lineEdit_25 = 0.0
        self.lineEdit_27 = 0.0
        self.lineEdit_28 = 0.0
        self.lineEdit_3 = 0.0
        self.lineEdit_4 = 0.0
        self.lineEdit_5 = 0.0
        self.lineEdit_6 = 0.0
        self.lineEdit_7 = 0.0
        self.lineEdit_8 = 0.0
        self.lineEdit_9 = 0.0
        self.galt = 0.0
        self.glong = 0.0
        self.glat = 0.0


    def start_server(self):
        print("Button pressed")

    def submit(self):
        print("Button Clickecd")

    def realtimeprocessing(self):
        print("Button Clickecd")

    def connectdrone1(self):
        print("Button Clickecd")

    def connectdrone2(self):
        print("Button Clickecd")

    def openmp1(self):
        print("Button Clickecd")

    def openmp2(self):
        print("Button Clickecd")

    def triangulate(self):
        print("Button Clickecd")

    def display(self):
        print("Button Clickecd")

    def storedata(self):
        print("Button Clickecd")

    def fpv1(self):
        print("Button Clickecd")

    def fpv2(self):
        self.val = "button clicked"
        self.lineEdit_9.setText(self.val)

    def close(self):
        sys.exit(0)

app = QApplication(sys.argv)
window = groundstat()
window.show()
sys.exit(app.exec_())


