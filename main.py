import sys,os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication,QDialog,QFileDialog,QInputDialog
import bgimgw
from PyQt5 import QtCore
import subprocess
import time as tm
import csv,time
import datetime

import socket
from threading import Thread
from socketserver import ThreadingMixIn

##currenttime = datetime.datetime.now()
##currenttime = str(currenttime)
##currenttime_array = currenttime.split(' ')
##date = currenttime_array[0]
##time = currenttime_array[1][:8]
##mode = time.split(':')
##s1 = int(mode[0])
##s2 = int(mode[1])
##s3 = int(mode[2])
##s1 = s1*10000+s2*100+s3
##time = s1
##mode = date.split('-')
##s1 = int(mode[0])
##s2 = int(mode[1])
##s3 = int(mode[2])
##s1 = s1*10000+s2*100+s3
##date = s1
##filename = 'output'+str(time)+'_'+str(date)
##filename+='.csv'
##print('Name of File created :',filename)
##header_name = ["Date","Time","PM1","PM2.5","PM10","NO2","CO2","CO","Humidity","Temperature"]
##with open(filename, 'w+') as csv_file:
##    csv_writer = csv.writer(csv_file)
##    csv_writer.writerow(header_name)


class GroundStat(QMainWindow):

    def __init__(self):
        super(GroundStat, self).__init__()
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
        self.pushButton_10.clicked.connect(self.closed)

        self.glatval = 0.0
        self.glongval = 0.0
        self.galtval = 0.0
##        self.lat1 = 0.0
##        self.long1 = 0.0
##        self.alt1 = 0.0
##        self.yawd1 = 0.0
##        self.pitchd1 = 0.0
##        self.yawc1 = 0.0
##        self.pitchc1 = 0.0
##        self.yawt1 = 0.0
##        self.pitcht1 = 0.0
##        self.lat2 = 0.0
##        self.long2 = 0.0
##        self.alt2 = 0.0
##        self.yawd2 = 0.0
##        self.pitchd2 = 0.0
##        self.yawc2 = 0.0
##        self.pitchc2 = 0.0
##        self.yawt2 = 0.0
##        self.pitcht2 = 0.0
        self.mess = " "
        self.storeval = ''

    def submit(self):
        self.glatval = self.glat.toPlainText()
        self.glongval = self.glong.toPlainText()
        self.galtval = self.galt.toPlainText()
        self.mess = "Ground parameters received."+"Ground Lat: "+str(self.glatval)+" Ground Lng: "+str(self.glongval)+" Ground Alt: "+str(self.galtval)
        self.message.setText(self.mess)

    def postprocessing(self):
        self.open_dialog_box()

    def realtimeprocessing(self):
        self.mess = "Host Ground Station as a server to the Drone."
        self.message.setText(self.mess)
    def connectdrone1(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.printhi)
        timer.setInterval(1)
        timer.start()

    def connectdrone2(self):
        print("aa")
        
    def connectdronea(self,conn1):
        while True:
            data = conn1.recv(2048)
            message = data.decode()
            message_array = message.split(",")
            #if (len(message_array) != 7):
             #   continue
            print(message)

    def connectdroneb(self,conn2):
        while True:
            data = conn2.recv(2048)
            message = data.decode()
            message_array = message.split(",")
            #if (len(message_array) != 7):
            #   continue
            print(message)

    def startserver(self):
        TCP_IP = '192.168.1.104'
        TCP_PORT = 2004
        buffersize = 20
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpServer.bind((TCP_IP, TCP_PORT))

        while True:
            tcpServer.listen(4)
            self.mess = "Ground Station Server waiting for Drone1 and Drone2"
            self.message.setText(self.mess)
            print(self.mess)
            (conn1, (ip, port)) = tcpServer.accept()
            self.mess = "Drone1 connected."
            self.message.setText(self.mess)
            Thread(target=self.connectdronea(conn1)).start()
            (conn2, (ip, port)) = tcpServer.accept()
            self.mess = "Drone2 connected."
            self.message.setText(self.mess)
            Thread(target=self.connectdroneb(conn2)).start()

    def openmp1(self):
        self.message.setText("Opening Mission Planner..")
        time.sleep(1.5)
        subprocess.Popen("C:\Program Files (x86)\Mission Planner\MissionPlanner.exe")

        self.message.setText("Mission Planner opened for drone 1")

    def openmp2(self):
        self.message.setText("Opening Mission Planner..")
        time.sleep(1.5)
        subprocess.Popen("C:\Program Files (x86)\Mission Planner\MissionPlanner.exe")

        self.message.setText("Mission Planner opened for drone 2")

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        filename = filename[0]
        print(filename)
        #filename = 'C:/Users/ARGHA SEN/Desktop/example1.txt'
        flag = 0
        i=0
        with open(filename, "r") as infile:
            read = csv.reader(infile)


            for row in read:
                i+=1
                try:
                    self.storeval = row
                    self.storeval.append(i)
                    # self.timer = QtCore.QTimer()

                    # self.timer.timeout.connect(self.printhi)

                    # self.timer.start(1000)
                    #self.timer.setInterval(100, self.printhi)
                    #self.update_val(row)
                    #self.printhi()
                    #print(row)
                    print(i)

                    
                except Exception as e:
                    print("Update error: ",e)
                #self.timer.timeout.connect(self.update_val(row))

    def printhi(self):
        print("Hi")
        print(self.storeval)

    def update_val(self,row):
        self.lat1.setText(row[2])
        self.long1.setText(row[3])
        self.alt1.setText(row[4])
        self.yawd1.setText(row[5])
        self.pitchd1.setText(row[6])
        self.yawc1.setText(row[7])
        self.pitchc1.setText(row[8])
        self.yawt1.setText(row[9])
        self.pitcht1.setText(row[10])
        self.lat2.setText(row[11])
        self.long2.setText(row[12])
        self.alt2.setText(row[13])
        self.yawd2.setText(row[14])
        self.pitchd2.setText(row[15])
        self.yawc2.setText(row[16])
        self.pitchc2.setText(row[17])
        self.yawt2.setText(row[18])
        self.pitcht2.setText(row[19])
        print(row[2])
        return

    def triangulate(self):
        print("button clicked")

    def display(self):
        print("button clicked")

    def storedata(self):
        self.mess = "Name of the "
        self.message.setText(self.mess)

    def fpv1(self):
        print("button clicked")

    def fpv2(self):
        print("button clicked")

    def closed(self):
        for t in threads:
            t.join()
        sys.exit(0)

app = QApplication(sys.argv)
window = GroundStat()
window.show()
sys.exit(app.exec_())




