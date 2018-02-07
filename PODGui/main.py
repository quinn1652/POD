import sys
import PyQt5
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import mainwindow_auto
import groupsettings_auto

import requests
import threading

import os
import time

class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    connectedPods = []
    groups = []
    expName = ""
    expDur = 0
    expPhotos = 0
    expWater = 0

    expRunning = False
    expPods = dict({})
    
    def __init__(self):          
        #initial window setup
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.imgPOD.setStyleSheet('border-image: url("LogoWhite.png")')

        if os.path.isfile("experiment.txt"):
            self.initExperimentInfo()


        #self.updateAvailable()
        self.pressedExperimentInfo()
        
        #buttonPressFunctions
        self.btnExperimentInfo.clicked.connect(lambda: self.pressedExperimentInfo())
        self.btnNew.clicked.connect(lambda: self.pressedNew())
        self.btnHelp.clicked.connect(lambda: self.pressedPodInfo())
        self.btnNext.clicked.connect(lambda: self.pressedNext())
        self.btnAddGroup.clicked.connect(lambda: self.pressedAddGroup())
        self.btnGroupStart.clicked.connect(lambda: self.pressedStart())
        self.btnGroupBack.clicked.connect(lambda: self.pressedGroupBack())
        self.btn_exp_cancel.clicked.connect(lambda: self.pressedCancel())
        self.lst_exp_pods.itemClicked.connect(lambda: self.selectedExpItem())

    def pressedCancel(self):
        #stop the experiment
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Are you sure you want to cancel the experiment? This cannot be undone!")
        msg.setWindowTitle("Cancel Experiment?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        cont = msg.exec_()
        if cont == QMessageBox.Yes:
            os.remove("experiment.txt")
            MainWindow.expRunning = False
            self.pressedExperimentInfo()

    def selectedExpItem(self):
        item = self.lst_exp_pods.currentItem().text()
        self.updatePodInfo(item)

    def updatePodInfo(self, item):
        _translate = QtCore.QCoreApplication.translate
        values = MainWindow.expPods[item]
        self.frm_light.setStyleSheet("background-color: rgb(128, 255, 107);")
        self.frm_overall.setStyleSheet("background-color: rgb(128, 255, 107);")
        self.frm_temp.setStyleSheet("background-color: rgb(128, 255, 107);")
        self.frm_network.setStyleSheet("background-color: rgb(128, 255, 107);")
        if values.getOverall() == False:
            self.frm_overall.setStyleSheet("background-color: rgb(239, 41, 41);")

        if values.getLight() == False:
            self.frm_light.setStyleSheet("background-color: rgb(239, 41, 41);")

        if values.getTemp() == False:
            self.frm_temp.setStyleSheet("background-color: rgb(239, 41, 41);")

        if values.getNetwork() == False:
            self.frm_network.setStyleSheet("background-color: rgb(239, 41, 41);")

        self.lbl_on_sec.setText(str(values.getOn()) + "s")
        self.lbl_off_sec.setText(str(values.getOff()) + "s")
        self.lbl_brightness_percent.setText(str(values.getBright()) + "%")
        self.lbl_exp_podid.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">" + values.getName() + "</span></p></body></html>"))

    def initExperimentInfo(self):
        MainWindow.expRunning = True
        expFile = open("experiment.txt", "r")
        MainWindow.expName = expFile.readline()
        MainWindow.expDur = int(expFile.readline())
        MainWindow.expPhotos = int(expFile.readline())
        MainWindow.expWater = float(expFile.readline())
            
    def pressedExperimentInfo(self):
        #set page to experiment info page
        if MainWindow.expRunning:
            self.lst_exp_pods.clear()
            _translate = QtCore.QCoreApplication.translate
            self.stackedWidget.setCurrentIndex(4)
            self.lbl_exp_name.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">" + MainWindow.expName + "</span></p></body></html>"))
            self.lbl_exp_day.setText("Day: " + str(1) + "/" + str(30))
            #check for what pods are in experiment
            self.getPodExperimentInfo()
        else:
            self.stackedWidget.setCurrentIndex(0)

    def getPodExperimentInfo(self):
        expFile = open("experiment.txt", "r")
        for line in expFile: 
            podstatus = line.split(",")
            if len(podstatus) > 1:
                nameSplit = podstatus[0].split(" ")
                podNum = int(nameSplit[1])
                try:
                    lightFile = open("PODDATA/" + str(podNum) + "-light")
                    tempFile = open("PODDATA/" + str(podNum) + "-temp")
                    lines = lightFile.readlines()
                    lightFile.close()
                    last_line = lines[len(lines) -1]
                    lightOk = False
                    tempOk = False
                    if last_line != "-1\n":
                        lightOk = True
                    
                    lines = tempFile.readlines()
                    tempFile.close()
                    last_line = lines[-1]

                    if last_line != "-1\n":
                        tempOk = True

                    podName = podstatus[0]
                    podOn = podstatus[1]
                    podOff = podstatus[2]
                    podBright = podstatus[3].rstrip()

                    podNetwork = False
                    print(podstatus[0])
                    if podstatus[0] in MainWindow.connectedPods:
                        print("yooooo")
                        podNetwork = True
                
                    MainWindow.expPods[podName] = PodValues(podName, podOn, podOff, podBright,
                                                    lightOk, tempOk, podNetwork)

                    self.lst_exp_pods.addItem(podName)
                except:
                    print("woah buddy")
        
    def pressedNew(self):
        #set page to new experiment page
        self.stackedWidget.setCurrentIndex(1)

    def pressedPodInfo(self):
        #set page to pod info page
        self.stackedWidget.setCurrentIndex(3)

    def pressedNext(self):
        if len(self.txtName.toPlainText()) > 0:
            #set page to group assignings
            self.stackedWidget.setCurrentIndex(2)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please Enter an Experiment Name")
            msg.setWindowTitle("No Experiment Name")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def pressedAddGroup(self):
        dialog = GroupSettingsDialog()
        dialog.show()

        #get return values from group settings dialog
        retval = dialog.exec_()
        groupName = dialog.getName()
        lightOn = dialog.getLightOn()
        lightOff = dialog.getLightOff()
        brightness = dialog.getBrightness()

        print(groupName)

        if retval == 1:
            #ok
            newLbl = QLabel(self)
            newLbl.setText(groupName)
            newLst = QListWidget(self)
            newLst.setMinimumWidth(200)
            newLst.setMaximumWidth(200)
            newLst.setDragDropMode(QAbstractItemView.DragDrop)
            newLst.setDefaultDropAction(Qt.MoveAction)

            MainWindow.groups.append(PodGroup(newLst, lightOn, lightOff, brightness))
            
            newGroupLayout = QVBoxLayout(self)
            newGroupLayout.setContentsMargins(1,1,1,1)
            newGroupLayout.addWidget(newLbl, 0, QtCore.Qt.AlignLeft)
            newGroupLayout.addWidget(newLst, 0, QtCore.Qt.AlignLeft)

            self.lyt_scroll.addLayout(newGroupLayout)

    def pressedGroupBack(self):
        self.stackedWidget.setCurrentIndex(1)
        
    def pressedStart(self):
        #check if there are still unassigned pods, warn user
        cont = QMessageBox.Yes
        if self.lstUnassigned.count() > 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("There are unassigned PODs, continue anyway?")
            msg.setWindowTitle("Unassigned PODs")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            cont = msg.exec_()

        #save out experiment data to file
        if cont == QMessageBox.Yes:
            MainWindow.expName = self.txtName.toPlainText()
            MainWindow.expDur = self.spnDays.value()
            MainWindow.expPhotos = self.spnPhotos.value()
            MainWindow.expWater = self.spnWater.value()

            expFile = open("experiment.txt", "w")
            expFile.write(MainWindow.expName + "\n")
            expFile.write(str(MainWindow.expDur) + "\n")
            expFile.write(str(MainWindow.expPhotos) + "\n")
            expFile.write(str(MainWindow.expWater) + "\n")
            expFile.write(str(time.time()) + "\n")
            expFile.write(str(time.time() + 24*60*60*MainWindow.expDur) + "\n")
            
            for g in MainWindow.groups:
                groupList = g.getGroupList()

                for i in range(groupList.count()):
                    expFile.write(groupList.item(i).text() + "," + str(g.getLightOn()) + ","
                                  + str(g.getLightOff()) + "," + str(g.getBrightness()) + "\n")

            expFile.close()
            MainWindow.expRunning = True
            self.pressedExperimentInfo()
            
    #called periodically to check how many PODs are connected
    def updateAvailable(self):
        #restart timer
        timer = threading.Timer(5, self.updateAvailable)
        timer.start()

        #ask webserver how many are connected
        host = 'http://localhost/getConnected.php'
        try:
            r = requests.get(host)
            print(r.text)
            
            #update label
            connected = r.text.split('\n')
            self.lblAvailable.setText(str(len(connected) - 1) + " Available")
            
            #add and remove items as fit
            if len(MainWindow.connectedPods) == 0:
                self.addItems(connected)
            else:
                self.removeItems(set(MainWindow.connectedPods) - set(connected))
                self.addItems(set(connected) - set(MainWindow.connectedPods))
                
            MainWindow.connectedPods = connected
            
        except:
            print("hello!")
            self.lblAvailable.setText("No Network")
            self.removeItems(MainWindow.connectedPods)
            


    def removeItems(self, toRemove):
        #goes through toRemove, searches listWidget for items and removes them
        for r in toRemove:
            items = self.lstUnassigned.findItems(r, Qt.MatchExactly)
            for l in items:
                self.lstUnassigned.takeItem(self.lstUnassigned.row(l))

    def addItems(self, toAdd):
        #goes through toAdd and adds an item to listWidget for each item
        for a in toAdd:
            #kills the trailing \n
            if len(a) > 0:
                self.lstUnassigned.addItem(a)

        #sort finished list
        self.lstUnassigned.sortItems(Qt.AscendingOrder)



class GroupSettingsDialog(QDialog, groupsettings_auto.Ui_Dialog):
    def __init__(self):
        #initial window setup
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.dlgButton.accepted.connect(lambda: self.okClicked())
        self.dlgButton.rejected.connect(lambda: self.cancelClicked())
        self.rad_on.toggled.connect(lambda: self.onClicked(self.rad_on.isChecked()))
        self.rad_off.toggled.connect(lambda: self.offClicked(self.rad_off.isChecked()))
        self.rad_mix.toggled.connect(lambda: self.mixClicked(self.rad_mix.isChecked()))

    def onClicked(self, enabled):
        if enabled:
            self.spnLightOff.setEnabled(False)
            self.spnLightOn.setEnabled(False)
            self.spnLightOn.setValue(1.0)
            self.spnLightOff.setValue(0)

    def offClicked(self, enabled):
        if enabled:
            self.spnLightOff.setEnabled(False)
            self.spnLightOn.setEnabled(False)
            self.spnLightOn.setValue(0)
            self.spnLightOff.setValue(1.0)

    def mixClicked(self, enabled):
        if enabled:
            self.spnLightOff.setEnabled(True)
            self.spnLightOn.setEnabled(True)
        
    def getName(self):
        return self.txtGroupName.toPlainText()

    def getLightOn(self):
        return self.spnLightOn.value()
    
    def getLightOff(self):
        return self.spnLightOff.value()

    def getBrightness(self):
        #spinbox is brightness box, haven't renamed it because I'm dumb
        return self.spinBox.value()
    
    def okClicked(self):
        self.done(1)
        
    def cancelClicked(self):
        self.done(0)

class PodValues():
    def __init__(self, name, on, off, bright, light, temp, network):
        self.name = name
        self.on = on
        self.off = off
        self.bright = bright
        self.light = light
        self.temp = temp
        self.network = network
        self.overall = False
        if self.light == True and self.temp == True and self.network == True:
            self.overall = True

    def getOn(self):
        return self.on

    def getOff(self):
        return self.off

    def getBright(self):
        return self.bright

    def getLight(self):
        return self.light

    def getTemp(self):
        return self.temp

    def getNetwork(self):
        return self.network

    def getOverall(self):
        return self.overall

    def getName(self):
        return self.name

class PodGroup():
    def __init__(self, groupList, on, off, brightness):
        self.groupList = groupList
        self.lightOn = on
        self.lightOff = off
        self.brightness = brightness

    def getGroupList(self):
        return self.groupList

    def getLightOn(self):
        return self.lightOn

    def getLightOff(self):
        return self.lightOff

    def getBrightness(self):
        return self.brightness
        
def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.updateAvailable()
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
