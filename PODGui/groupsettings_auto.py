# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupsettings.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(445, 253)
        Dialog.setAcceptDrops(False)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.lblGroupSettings = QtWidgets.QLabel(Dialog)
        self.lblGroupSettings.setObjectName("lblGroupSettings")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblGroupSettings)
        self.lblGroupName = QtWidgets.QLabel(Dialog)
        self.lblGroupName.setObjectName("lblGroupName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lblGroupName)
        self.txtGroupName = QtWidgets.QTextEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtGroupName.sizePolicy().hasHeightForWidth())
        self.txtGroupName.setSizePolicy(sizePolicy)
        self.txtGroupName.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtGroupName.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtGroupName.setTabChangesFocus(True)
        self.txtGroupName.setObjectName("txtGroupName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtGroupName)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setMinimumSize(QtCore.QSize(0, 36))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 1, -1, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.rad_on = QtWidgets.QRadioButton(self.widget)
        self.rad_on.setMaximumSize(QtCore.QSize(100, 16777215))
        self.rad_on.setChecked(False)
        self.rad_on.setObjectName("rad_on")
        self.horizontalLayout.addWidget(self.rad_on, 0, QtCore.Qt.AlignRight)
        self.rad_off = QtWidgets.QRadioButton(self.widget)
        self.rad_off.setMaximumSize(QtCore.QSize(100, 16777215))
        self.rad_off.setObjectName("rad_off")
        self.horizontalLayout.addWidget(self.rad_off)
        self.rad_mix = QtWidgets.QRadioButton(self.widget)
        self.rad_mix.setMaximumSize(QtCore.QSize(53, 16777215))
        self.rad_mix.setChecked(True)
        self.rad_mix.setObjectName("rad_mix")
        self.horizontalLayout.addWidget(self.rad_mix)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.widget)
        self.lblLightON = QtWidgets.QLabel(Dialog)
        self.lblLightON.setObjectName("lblLightON")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.lblLightON)
        self.spnLightOn = QtWidgets.QDoubleSpinBox(Dialog)
        self.spnLightOn.setEnabled(True)
        self.spnLightOn.setReadOnly(False)
        self.spnLightOn.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spnLightOn.setSingleStep(0.5)
        self.spnLightOn.setProperty("value", 1.0)
        self.spnLightOn.setObjectName("spnLightOn")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.spnLightOn)
        self.lblLightOff = QtWidgets.QLabel(Dialog)
        self.lblLightOff.setObjectName("lblLightOff")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.lblLightOff)
        self.spnLightOff = QtWidgets.QDoubleSpinBox(Dialog)
        self.spnLightOff.setSingleStep(0.5)
        self.spnLightOff.setProperty("value", 1.0)
        self.spnLightOff.setObjectName("spnLightOff")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.spnLightOff)
        self.dlgButton = QtWidgets.QDialogButtonBox(Dialog)
        self.dlgButton.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dlgButton.setObjectName("dlgButton")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.dlgButton)
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setMaximum(100)
        self.spinBox.setProperty("value", 50)
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "New Group"))
        self.lblGroupSettings.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:16pt;\">New Group Settings</span></p></body></html>"))
        self.lblGroupName.setText(_translate("Dialog", "Group Name:"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:14pt;\">Light</span></p></body></html>"))
        self.rad_on.setText(_translate("Dialog", "Always On"))
        self.rad_off.setText(_translate("Dialog", "Always Off"))
        self.rad_mix.setText(_translate("Dialog", "Mix"))
        self.lblLightON.setText(_translate("Dialog", "Light On (Seconds)"))
        self.lblLightOff.setText(_translate("Dialog", "Light Off (Seconds)"))
        self.label_2.setText(_translate("Dialog", "Brightness (Percentage of Max)"))
