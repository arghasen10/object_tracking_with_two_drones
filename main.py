import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d




class MainPage(QDialog):
    def __init__(self):
        super(MainPage,self).__init__()
        loadUi('home.ui',self)
        self.pushButton.clicked.connect(self.retrieve)

    def retrieve(self):
        x = self.plainTextEdit.toPlainText()
        y = self.plainTextEdit_2.toPlainText()
        z = self.plainTextEdit_3.toPlainText()

        self.textEdit.setText(x)
        self.textEdit_2.setText(y)
        self.textEdit_3.setText(z)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        xs = x.split(',')
        ys = y.split(',')
        zs = z.split(',')
        xs = [int(valx) for valx in xs]
        ys = [int(valy) for valy in ys]
        zs = [int(valz) for valz in zs]

        ax.plot(xs,ys,zs)

        plt.show()



app = QApplication(sys.argv)
widget = MainPage()
widget.show()
sys.exit(app.exec_())