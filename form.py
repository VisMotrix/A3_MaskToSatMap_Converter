# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QTextEdit, QVBoxLayout, QWidget)

from qtexteditlogger import QTextEditLogger

class Ui_guiMain(object):
    def setupUi(self, guiMain):
        if not guiMain.objectName():
            guiMain.setObjectName(u"guiMain")
        guiMain.resize(612, 400)
        self.actionLicense = QAction(guiMain)
        self.actionLicense.setObjectName(u"actionLicense")
        self.actionVerbose_Output = QAction(guiMain)
        self.actionVerbose_Output.setObjectName(u"actionVerbose_Output")
        self.actionVerbose_Output.setCheckable(True)
        self.centralwidget = QWidget(guiMain)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.layerPathEdit = QLineEdit(self.centralwidget)
        self.layerPathEdit.setObjectName(u"layerPathEdit")
        self.layerPathEdit.setMinimumSize(QSize(400, 0))

        self.horizontalLayout.addWidget(self.layerPathEdit)

        self.openLayersBtn = QPushButton(self.centralwidget)
        self.openLayersBtn.setObjectName(u"openLayersBtn")

        self.horizontalLayout.addWidget(self.openLayersBtn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.maskPathEdit = QLineEdit(self.centralwidget)
        self.maskPathEdit.setObjectName(u"maskPathEdit")
        self.maskPathEdit.setMinimumSize(QSize(400, 0))

        self.horizontalLayout_2.addWidget(self.maskPathEdit)

        self.openMaskBtn = QPushButton(self.centralwidget)
        self.openMaskBtn.setObjectName(u"openMaskBtn")

        self.horizontalLayout_2.addWidget(self.openMaskBtn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.satmapPathEdit = QLineEdit(self.centralwidget)
        self.satmapPathEdit.setObjectName(u"satmapPathEdit")
        self.satmapPathEdit.setMinimumSize(QSize(400, 0))

        self.horizontalLayout_3.addWidget(self.satmapPathEdit)

        self.saveAsBtn = QPushButton(self.centralwidget)
        self.saveAsBtn.setObjectName(u"saveAsBtn")

        self.horizontalLayout_3.addWidget(self.saveAsBtn)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.noiseCombo = QComboBox(self.centralwidget)
        self.noiseCombo.addItem("")
        self.noiseCombo.addItem("")
        self.noiseCombo.addItem("")
        self.noiseCombo.setObjectName(u"noiseCombo")

        self.horizontalLayout_5.addWidget(self.noiseCombo)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_5.addWidget(self.line)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(0, 0))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.rLabel = QLabel(self.centralwidget)
        self.rLabel.setObjectName(u"rLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(10)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.rLabel.sizePolicy().hasHeightForWidth())
        self.rLabel.setSizePolicy(sizePolicy1)
        self.rLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.rLabel)

        self.gLabel = QLabel(self.centralwidget)
        self.gLabel.setObjectName(u"gLabel")
        sizePolicy.setHeightForWidth(self.gLabel.sizePolicy().hasHeightForWidth())
        self.gLabel.setSizePolicy(sizePolicy)
        self.gLabel.setMinimumSize(QSize(5, 0))
        self.gLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.gLabel)

        self.bLabel = QLabel(self.centralwidget)
        self.bLabel.setObjectName(u"bLabel")
        sizePolicy.setHeightForWidth(self.bLabel.sizePolicy().hasHeightForWidth())
        self.bLabel.setSizePolicy(sizePolicy)
        self.bLabel.setMinimumSize(QSize(10, 0))
        self.bLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.bLabel)


        self.horizontalLayout_5.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.rNoiseSpin = QSpinBox(self.centralwidget)
        self.rNoiseSpin.setObjectName(u"rNoiseSpin")
        self.rNoiseSpin.setMaximum(255)

        self.verticalLayout_2.addWidget(self.rNoiseSpin)

        self.gNoiseSpin = QSpinBox(self.centralwidget)
        self.gNoiseSpin.setObjectName(u"gNoiseSpin")
        self.gNoiseSpin.setMaximum(255)

        self.verticalLayout_2.addWidget(self.gNoiseSpin)

        self.bNoiseSpin = QSpinBox(self.centralwidget)
        self.bNoiseSpin.setObjectName(u"bNoiseSpin")
        self.bNoiseSpin.setMaximum(255)

        self.verticalLayout_2.addWidget(self.bNoiseSpin)


        self.horizontalLayout_5.addLayout(self.verticalLayout_2)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_5.addWidget(self.line_2)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.coverageSpin = QDoubleSpinBox(self.centralwidget)
        self.coverageSpin.setObjectName(u"coverageSpin")
        self.coverageSpin.setDecimals(1)
        self.coverageSpin.setMaximum(100.000000000000000)
        self.coverageSpin.setSingleStep(5.000000000000000)
        self.coverageSpin.setValue(5.000000000000000)

        self.horizontalLayout_5.addWidget(self.coverageSpin)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.startBtn = QPushButton(self.centralwidget)
        self.startBtn.setObjectName(u"startBtn")

        self.horizontalLayout_4.addWidget(self.startBtn)

        self.resultBtn = QPushButton(self.centralwidget)
        self.resultBtn.setObjectName(u"resultBtn")

        self.horizontalLayout_4.addWidget(self.resultBtn)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_4.addWidget(self.label_7)

        self.workDrivePathEdit = QLineEdit(self.centralwidget)
        self.workDrivePathEdit.setObjectName(u"workDrivePathEdit")

        self.horizontalLayout_4.addWidget(self.workDrivePathEdit)

        self.openPDrvBtn = QPushButton(self.centralwidget)
        self.openPDrvBtn.setObjectName(u"openPDrvBtn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.openPDrvBtn.sizePolicy().hasHeightForWidth())
        self.openPDrvBtn.setSizePolicy(sizePolicy2)
        self.openPDrvBtn.setMinimumSize(QSize(30, 0))
        self.openPDrvBtn.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_4.addWidget(self.openPDrvBtn)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.plainTextEdit = QTextEditLogger(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy3)
        self.plainTextEdit.setMinimumSize(QSize(0, 50))
        self.plainTextEdit.setUndoRedoEnabled(False)
        self.plainTextEdit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.plainTextEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.plainTextEdit)

        guiMain.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(guiMain)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 612, 21))
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        guiMain.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(guiMain)
        self.statusbar.setObjectName(u"statusbar")
        guiMain.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuAbout.addAction(self.actionLicense)
        self.menuAbout.addAction(self.actionVerbose_Output)

        self.retranslateUi(guiMain)

        QMetaObject.connectSlotsByName(guiMain)
    # setupUi

    def retranslateUi(self, guiMain):
        guiMain.setWindowTitle(QCoreApplication.translate("guiMain", u"ARMA3 - Mask to Sat Map Converter", None))
        self.actionLicense.setText(QCoreApplication.translate("guiMain", u"License", None))
        self.actionVerbose_Output.setText(QCoreApplication.translate("guiMain", u"Verbose Output", None))
        self.label.setText(QCoreApplication.translate("guiMain", u"Layer.cfg path", None))
#if QT_CONFIG(tooltip)
        self.layerPathEdit.setToolTip(QCoreApplication.translate("guiMain", u"Path to you layers config file", None))
#endif // QT_CONFIG(tooltip)
        self.openLayersBtn.setText(QCoreApplication.translate("guiMain", u"Open", None))
        self.label_2.setText(QCoreApplication.translate("guiMain", u"mask image path", None))
#if QT_CONFIG(tooltip)
        self.maskPathEdit.setToolTip(QCoreApplication.translate("guiMain", u"path to the mask image", None))
#endif // QT_CONFIG(tooltip)
        self.openMaskBtn.setText(QCoreApplication.translate("guiMain", u"Open", None))
        self.label_3.setText(QCoreApplication.translate("guiMain", u"Sat map output path", None))
#if QT_CONFIG(tooltip)
        self.satmapPathEdit.setToolTip(QCoreApplication.translate("guiMain", u"path to save resulting file to", None))
#endif // QT_CONFIG(tooltip)
        self.saveAsBtn.setText(QCoreApplication.translate("guiMain", u"Save as", None))
        self.label_4.setText(QCoreApplication.translate("guiMain", u"Noise Settings", None))
        self.noiseCombo.setItemText(0, QCoreApplication.translate("guiMain", u"No Noise", None))
        self.noiseCombo.setItemText(1, QCoreApplication.translate("guiMain", u"BW Noise", None))
        self.noiseCombo.setItemText(2, QCoreApplication.translate("guiMain", u"RGB Noise", None))

#if QT_CONFIG(tooltip)
        self.noiseCombo.setToolTip(QCoreApplication.translate("guiMain", u"<html><head/><body><p>Noise type:</p><p>No Noise - Just replace colors</p><p>BW Noise - Create noise in pixel brightness</p><p>RGB Noise- Create noise in rgb values</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("guiMain", u"Noise strength", None))
        self.rLabel.setText(QCoreApplication.translate("guiMain", u"R", None))
        self.gLabel.setText(QCoreApplication.translate("guiMain", u"G", None))
        self.bLabel.setText(QCoreApplication.translate("guiMain", u"B", None))
#if QT_CONFIG(tooltip)
        self.rNoiseSpin.setToolTip(QCoreApplication.translate("guiMain", u"Variation for Red channel", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.gNoiseSpin.setToolTip(QCoreApplication.translate("guiMain", u"Variation for green channel / brightness", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.bNoiseSpin.setToolTip(QCoreApplication.translate("guiMain", u"Variation for blue channel", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("guiMain", u"Noise Coverage", None))
#if QT_CONFIG(tooltip)
        self.coverageSpin.setToolTip(QCoreApplication.translate("guiMain", u"<html><head/><body><p>How much area will be affected by the noise.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.coverageSpin.setSuffix(QCoreApplication.translate("guiMain", u"%", None))
#if QT_CONFIG(tooltip)
        self.startBtn.setToolTip(QCoreApplication.translate("guiMain", u"Start mask processing", None))
#endif // QT_CONFIG(tooltip)
        self.startBtn.setText(QCoreApplication.translate("guiMain", u"Start", None))
#if QT_CONFIG(tooltip)
        self.resultBtn.setToolTip(QCoreApplication.translate("guiMain", u"Open folder of output file", None))
#endif // QT_CONFIG(tooltip)
        self.resultBtn.setText(QCoreApplication.translate("guiMain", u"Open Result", None))
        self.label_7.setText(QCoreApplication.translate("guiMain", u"A3 Tools Work drive", None))
#if QT_CONFIG(tooltip)
        self.workDrivePathEdit.setToolTip(QCoreApplication.translate("guiMain", u"the location of you Arma3 tools etc. ", None))
#endif // QT_CONFIG(tooltip)
        self.workDrivePathEdit.setText(QCoreApplication.translate("guiMain", u"P:\\", None))
        self.openPDrvBtn.setText(QCoreApplication.translate("guiMain", u"...", None))
        self.menuAbout.setTitle(QCoreApplication.translate("guiMain", u"Help", None))
    # retranslateUi

