import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.uic import loadUi
#from gimbal_plot import parse



class MainPage(QDialog):
    def __init__(self):
        super(MainPage,self).__init__()
        loadUi('home.ui',self)
        self.pushButton.clicked.connect(self.retrievedrone1)
        self.pushButton_2.clicked.connect(self.retrievedrone2)
        self.pushButton_3.clicked.connect(self.plot_lines)
        self.lat1val = 0.0
        self.lat2val = 0.0
        self.lon1val = 0.0
        self.lon2val = 0.0
        self.alt1val = 0.0
        self.alt2val = 0.0
        self.pitchval1val = 0.0
        self.yawval1val = 0.0
        self.pitchval2val = 0.0
        self.yawval2val = 0.0

    def retrievedrone1(self):
        self.lat1val = self.lat1.toPlainText()
        self.lon1val = self.lon1.toPlainText()
        self.alt1val = self.alt1.toPlainText()
        self.pitchval1val = self.pitchval1.toPlainText()
        self.yawval1val = self.yawval1.toPlainText()

        self.textEdit.setText(self.lat1val)
        self.textEdit_2.setText(self.lon1val)
        self.textEdit_3.setText(self.alt1val)
        self.textEdit_4.setText(self.pitchval1val)
        self.textEdit_5.setText(self.yawval1val)


    def retrievedrone2(self):
        self.lat2val = self.lat2.toPlainText()
        self.lon2val = self.lon2.toPlainText()
        self.alt2val = self.alt2.toPlainText()
        self.pitchval2val = self.pitchval2.toPlainText()
        self.yawval2val = self.yawval2.toPlainText()

        self.textEdit_6.setText(self.lat2val)
        self.textEdit_7.setText(self.lon2val)
        self.textEdit_8.setText(self.alt2val)
        self.textEdit_9.setText(self.pitchval2val)
        self.textEdit_10.setText(self.yawval2val)





    def plot_lines(self):
        import gimbal_plot
        self.lat1val = float(self.lat1val)
        self.lon1val = float(self.lon1val)
        self.alt1val = float(self.alt1val)
        self.pitchval1val = float(self.pitchval1val)
        self.yawval1val = float(self.yawval1val)
        self.lat2val = float(self.lat2val)
        self.lon2val = float(self.lon2val)
        self.alt2val = float(self.alt2val)
        self.pitchval2val = float(self.pitchval2val)
        self.yawval2val = float(self.yawval2val)

        parser = gimbal_plot.parse(self.lat1val,self.lon1val,self.alt1val,self.pitchval1val,self.yawval1val,self.lat2val,self.lon2val,self.alt2val,self.pitchval2val,self.yawval2val)



app = QApplication(sys.argv)
widget = MainPage()
widget.show()
sys.exit(app.exec_())