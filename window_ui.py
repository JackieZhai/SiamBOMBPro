# Created by: PyQt5 UI code generator 5.10.1
# Modified by: JackieZhai on Feb 20 2020. All Rights Reserved.

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint

class Rect:
    def __init__(self):
        self.start = QPoint()
        self.end = QPoint()
    def setStart(self, s):
        self.start = s
    def setEnd(self, e):
        self.end = e
    def startPoint(self):
        return self.start
    def endPoint(self):
        return self.end
    def paint(self, painter):
        painter.drawRect(self.startPoint().x(), self.startPoint().y(),
                         self.endPoint().x() - self.startPoint().x(),
                         self.endPoint().y() - self.startPoint().y())

class Ui_MainWindow(QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setMouseTracking(True)
        self.setWindowTitle("Second Test")
        self.lastPoint = QPoint()
        self.endPoint = QPoint()
        # 存储b-box坐标信息
        self.bbox_list = []
        # 辅助画布
        self.pp = QPainter()
        self.paint_frame = None
        self.tempPix = QPixmap(800, 600)
        self.tempPix.fill(Qt.white)
        self.shape = None
        self.rectList = []
        self.perm = False
        # 是否处于绘制阶段
        self.isPainting = False
        # 是否处于初始化阶段
        self.first_frame = False
        # 目前状态 Suspending|Location|Video|Camera = 0|1|2|3
        self.isStatus = 0
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1350, 725)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label_image = QtWidgets.QLabel(self.centralwidget)
        self.label_image.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.label_image.setObjectName("label_3")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(825, 25, 500, 700))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_locationLoading = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_locationLoading.setObjectName("pushButton_locationLoading")
        self.horizontalLayout.addWidget(self.pushButton_locationLoading)
        self.pushButton_videoLoading = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_videoLoading.setObjectName("pushButton_videoLoading")
        self.horizontalLayout.addWidget(self.pushButton_videoLoading)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton_cameraLoading = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_cameraLoading.setObjectName("pushButton_cameraLoading")
        self.verticalLayout.addWidget(self.pushButton_cameraLoading)
        self.pushButton_bboxSetting = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_bboxSetting.setObjectName("pushButton_bboxSetting")
        self.verticalLayout.addWidget(self.pushButton_bboxSetting)
        self.pushButton_algorithmProcessing = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_algorithmProcessing.setObjectName("pushButton_algorithmProcessing")
        self.verticalLayout.addWidget(self.pushButton_algorithmProcessing)
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.horizontalLayout_select = QtWidgets.QHBoxLayout()
        self.horizontalLayout_select.setObjectName("horizontalLayout_select")
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_select.addWidget(self.spinBox)
        self.label_spinBox = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_spinBox.setMaximumSize(10000, 45)
        self.label_spinBox.setText('Analysis Object Selecting')
        self.horizontalLayout_select.addWidget(self.label_spinBox)
        self.horizontalLayout_select.setStretch(1, 1)
        self.horizontalLayout_select.setStretch(2, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_select)
        self.label_bbox = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_bbox.setAlignment(Qt.AlignCenter)
        self.label_bbox.setWordWrap(True)
        self.verticalLayout.addWidget(self.label_bbox)
        self.label_source = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_source.setAlignment(Qt.AlignCenter)
        self.label_source.setWordWrap(True)
        self.verticalLayout.addWidget(self.label_source)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 20))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SiamBOMB"))
        self.pushButton_locationLoading.setText(_translate("MainWindow", "&Location Loading"))
        self.pushButton_locationLoading.setDefault(True)
        self.pushButton_videoLoading.setText(_translate("MainWindow", "&Video Loading"))
        self.pushButton_videoLoading.setDefault(True)
        self.pushButton_cameraLoading.setText(_translate("MainWindow", "&Camera Loading"))
        self.pushButton_cameraLoading.setDefault(True)
        self.pushButton_bboxSetting.setText(_translate("MainWindow", "&B-box Setting"))
        self.pushButton_bboxSetting.setDefault(True)
        self.pushButton_algorithmProcessing.setText(_translate("MainWindow", "&Algorithm Processing"))
        self.pushButton_algorithmProcessing.setDefault(True)
        self.checkBox.setText(_translate("MainWindow", "&Data Saving"))

    def paintEvent(self, event):
        if self.isPainting and self.perm:
            self.pp.begin(self.tempPix)
            pen = QPen(Qt.green, 6, Qt.SolidLine)
            self.pp.setPen(pen)
            for shape in self.rectList:
                shape.paint(self.pp)
            self.pp.end()
            label_text = ''
            for item in self.bbox_list:
                label_text += '\n'+str(item)
            self.label_bbox.setText(label_text)
            self.label_image.setPixmap(self.tempPix)

    def mousePressEvent(self, event):
        if self.isPainting:
            if event.button() == Qt.LeftButton:
                self.shape = Rect()
                if self.shape is not None:
                    self.perm = False
                    self.rectList.append(self.shape)
                    self.shape.setStart(event.pos())
                    self.shape.setEnd(event.pos())
                self.update()

    def mouseReleaseEvent(self, event):
        if self.isPainting:
            if event.button() == Qt.LeftButton:
                self.bbox_list.append((self.shape.startPoint().x(),
                                       self.shape.startPoint().y(),
                                       self.shape.endPoint().x()-self.shape.startPoint().x(),
                                       self.shape.endPoint().y()-self.shape.startPoint().y()))
                self.perm = True
                self.shape = None
                self.update()

    def mouseMoveEvent(self, event):
        if self.isPainting:
            self.endPoint = event.pos()
            if event.buttons() & Qt.LeftButton:
                if self.shape is not None and not self.perm:
                    self.shape.setEnd(event.pos())
                    self.update()