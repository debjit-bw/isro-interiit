# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphSheet.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot, LinearRegionItem
import json
import sys, os

path_to_file = f'{os.getcwd()}/{sys.argv[0]}'
path = path_to_file.split('/')
path.pop()
path.pop()
print(path)
finalPath = ""
for name in path:
    finalPath = finalPath + name + '/'
print(finalPath)
sys.path.insert(1, finalPath)

from backend import main

import os


class GraphSheet(object):
    OpenFiles = []
    index: int = 1

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Graph-Sheet")
        MainWindow.resize(773, 445)
        MainWindow.setStyleSheet(
            "background-color: #000;"
            "color: #FFF;"
        )

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.centralwidget.setLayout(QtWidgets.QVBoxLayout(self.centralwidget))
        self.centralwidget.layout().setContentsMargins(10, 10, 10, 10)

        self.ErrorBar = QtWidgets.QFrame(parent=self.centralwidget)
        self.ErrorBar.setLayout(QtWidgets.QHBoxLayout(self.ErrorBar))
        self.ErrorMsg = QtWidgets.QLabel("", parent=self.ErrorBar)
        self.ErrorMsg.setAlignment(QtCore.Qt.AlignHCenter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.ErrorMsg.sizePolicy().hasHeightForWidth())
        self.ErrorMsg.setSizePolicy(sizePolicy)
        self.ErrorMsg.setStyleSheet("background: transparent")
        self.Xbutton = MyButton(lambda: self.ErrorBar.setVisible(False))
        self.Xbutton.setIcon(QtGui.QIcon("close.png"))
        self.Xbutton.setStyleSheet("background: transparent")
        self.ErrorBar.layout().addWidget(self.ErrorMsg)
        self.ErrorBar.layout().addWidget(self.Xbutton, 0, QtCore.Qt.AlignRight)
        self.ErrorBar.setVisible(False)
        effect = QtWidgets.QGraphicsDropShadowEffect(self.ErrorBar)
        effect.setBlurRadius(10)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setColor(QtGui.QColor(200, 0, 0, 100))
        self.ErrorBar.setGraphicsEffect(effect)
        self.ErrorBar.setStyleSheet("background: rgba(200, 0, 0, 100)")
        self.Body = QtWidgets.QFrame(self.centralwidget)
        self.Body.setLayout(QtWidgets.QHBoxLayout(self.Body))
        self.Body.layout().setContentsMargins(0, 0, 0, 10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.Body.sizePolicy().hasHeightForWidth())
        self.centralwidget.layout().addWidget(self.ErrorBar, 0, QtCore.Qt.AlignTop)
        self.centralwidget.layout().addWidget(self.Body)

        self.SideBar = QtWidgets.QFrame(self.Body)
        self.SideBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SideBar.setLayout(QtWidgets.QVBoxLayout(self.SideBar))
        self.SideBar.setVisible(False)
        self.Body.layout().addWidget(self.SideBar, 0, QtCore.Qt.AlignLeft)

        self.Menu = QtWidgets.QFrame(self.SideBar)
        self.Menu.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Menu.setObjectName("Menu")
        self.Menu.setLayout(QtWidgets.QVBoxLayout(self.Menu))
        self.Menu.layout().setContentsMargins(5, 5, 5, 5)
        self.SideBar.layout().addWidget(
            self.Menu, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.Main = QtWidgets.QFrame(self.Body)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Main.sizePolicy().hasHeightForWidth())
        self.Main.setSizePolicy(sizePolicy)
        self.Main.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Main.setObjectName("Main")
        self.Main.setLayout(QtWidgets.QVBoxLayout(self.Main))
        self.Main.layout().setContentsMargins(9, 9, 9, 9)
        self.GraphHeader = QtWidgets.QFrame(self.Main)
        self.GraphHeader.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.GraphHeader.setFrameShadow(QtWidgets.QFrame.Raised)
        self.GraphHeader.setObjectName("GraphHeader")
        self.GraphHeader.setLayout(QtWidgets.QHBoxLayout(self.GraphHeader))

        self.MenuButton = MyButton(
            lambda: self.MenuButtonAction(), parent=self.GraphHeader)
        self.MenuButton.setAutoRaise(True)
        self.MenuButton.setObjectName("MenuButton")
        self.MenuButton.setIcon(QtGui.QIcon("menu.png"))
        self.FileButton = MyButton(
            lambda: self.FileButtonAction(), parent=self.GraphHeader)
        self.FileButton.setIcon(QtGui.QIcon("open-file-icon.png"))
        self.Title = QtWidgets.QLabel(
            "Identification Of Solar Bursts in X-Ray Light Curves")
        self.Title.setAlignment(QtCore.Qt.AlignHCenter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.Title.sizePolicy().hasHeightForWidth())
        self.Title.setSizePolicy(sizePolicy)

        self.GraphHeader.layout().addWidget(self.MenuButton)
        self.GraphHeader.layout().addWidget(self.Title)
        self.GraphHeader.layout().addWidget(self.FileButton, 0, QtCore.Qt.AlignRight)
        self.Main.layout().addWidget(self.GraphHeader)

        self.GraphArea = QtWidgets.QStackedWidget(self.Main)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.GraphArea.sizePolicy().hasHeightForWidth())
        self.GraphArea.setSizePolicy(sizePolicy)
        self.GraphArea.setFrameShape(QtWidgets.QFrame.Box)
        self.GraphArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.GraphArea.setObjectName("GraphArea")
        self.EmptyGraph = PlotWidget()
        self.EmptyGraph.setObjectName("EmptyGraph")
        self.GraphArea.addWidget(self.EmptyGraph)
        self.Main.layout().addWidget(self.GraphArea)
        self.Body.layout().addWidget(self.Main)
        MainWindow.setCentralWidget(self.centralwidget)

        self.FileMenu = QtWidgets.QFrame(self.Body)
        self.FileMenu.setLayout(QtWidgets.QVBoxLayout(self.FileMenu))
        self.AddFile = MyButton(lambda: self.AddFileAction(), self.FileMenu)
        self.AddFile.setText("Supported Formats")
        self.AddFile.setAutoRaise(True)
        self.AddFile.setStyleSheet("background: rgba(0, 0, 0, 50)")
        self.FileFormatList = QtWidgets.QFrame(self.FileMenu)
        self.FileFormatList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.FileFormatList.setLayout(
            QtWidgets.QVBoxLayout(self.FileFormatList))
        self.fitsButton = MyButton(
            lambda: self.Openfits(), parent=self.FileFormatList)
        self.fitsButton.setText("FITS")
        self.fitsHelp = QtWidgets.QLabel("The file should contain 2 elements, the second element being the main data. The data should be an array or list where the fields \"time\" and \"rate\" must be present. These should be the first 2 elements of each array.\nFor example, file[1] should be the main data, where file[1][0] should be of the form [<time_value>, <rate_value>] at least. The array can optionally contain the \"error\" and \"frace\" terms.")
        self.fitsHelp.setWordWrap(True)
        self.xlsButton = MyButton(
            lambda: self.Openxls(), parent=self.FileFormatList)
        self.xlsButton.setText("XLS")
        self.asciihelp = QtWidgets.QLabel("The file must contain rows of values of the form <time_value>, <rate_value>, [optionally, <error>, ,frace>] seperated by commas, for each data point. The data points need to be seperated by newlines.")
        self.asciihelp.setWordWrap(True)
        self.asciiButton = MyButton(
            lambda: self.Openascii(), parent=self.FileFormatList)
        self.asciiButton.setText("ASCII")
        self.xlshelp = QtWidgets.QLabel("SImilar to ASCII, the XLS file must have time in the first column and rate in the second column. The file can optionally contain error and frace in the third and fourth columns.\n")
        self.xlshelp.setWordWrap(True)
        self.FileFormatList.layout().addWidget(self.fitsButton, 0, QtCore.Qt.AlignTop)
        self.FileFormatList.layout().addWidget(self.fitsHelp, 0, QtCore.Qt.AlignTop)
        self.FileFormatList.layout().addWidget(self.asciiButton, 0, QtCore.Qt.AlignTop)
        self.FileFormatList.layout().addWidget(self.asciihelp, 0, QtCore.Qt.AlignTop)
        self.FileFormatList.layout().addWidget(self.xlsButton, 0, QtCore.Qt.AlignTop)
        self.FileFormatList.layout().addWidget(self.xlshelp, 0, QtCore.Qt.AlignTop)
        self.FileFormatList.setVisible(False)
        self.FileMenu.layout().addWidget(self.AddFile, 0, QtCore.Qt.AlignTop)
        self.FileMenu.layout().addWidget(self.FileFormatList, 0, QtCore.Qt.AlignTop)
        self.FileMenu.setVisible(False)
        self.Body.layout().addWidget(self.FileMenu, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def Openfits(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(directory=os.environ['HOME'])[0]
        if (fileName in self.OpenFiles) or fileName == "":
            return
        output = main.get_analysis_data(fileName, "fits")
        if(output['OK']['status']):
            self.addPlot(fileName.split('/')[-1], output)
            self.ErrorBar.setVisible(False)
            self.OpenFiles.append(fileName)
        else:
            self.ErrorMsg.setText(output['OK']['message'])
            self.ErrorBar.setVisible(True)

    def Openxls(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(directory=os.environ['HOME'])[0]
        if (fileName in self.OpenFiles) or fileName == "":
            return
        if(output['OK']['status']):
            self.addPlot(fileName.split('/')[-1], output)
            self.ErrorBar.setVisible(False)
            self.OpenFiles.append(fileName)
        else:
            self.ErrorMsg.setText(output['OK']['message'])
            self.ErrorBar.setVisible(True)

    def Openascii(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(directory=os.environ['HOME'])[0]
        if (fileName in self.OpenFiles) or fileName == "":
            return
        output = main.get_analysis_data(fileName, "ascii")
        if(output['OK']['status']):
            self.addPlot(fileName.split('/')[-1], output)
            self.ErrorBar.setVisible(False)
            self.OpenFiles.append(fileName)
        else:
            self.ErrorMsg.setText(output['OK']['message'])
            self.ErrorBar.setVisible(True)

    def FileButtonAction(self):
        self.FileMenu.setVisible(not self.FileMenu.isVisible())

    def AddFileAction(self):
        if(self.AddFile.styleSheet() == "background: rgba(0, 0, 0, 50)"):
            self.AddFile.setStyleSheet("background: rgba(255, 0 , 0, 50)")
        else:
            self.AddFile.setStyleSheet("background: rgba(0, 0, 0, 50)")
        self.FileFormatList.setVisible(not self.FileFormatList.isVisible())

    def MenuButtonAction(self):
        self.SideBar.setVisible(not self.SideBar.isVisible())

    def addPlot(self, name: str, jObject: dict):
        graphPoints = jObject['graph_data']
        peaks = jObject['peaks']
        mainGraph = PlotWidget()
        mainGraph.plot(range(0, len(graphPoints)), graphPoints)
        self.GraphArea.addWidget(mainGraph)
        subplotnames = []
        i = 1
        for obj in peaks:
            subplotnames.append(f'{name}_range_{i}')
            item = LinearRegionItem()
            graph = PlotWidget(parent=self.GraphArea)
            mainGraph.addItem(item)
            item.setRegion([obj["range"][0], obj["range"][1]])
            item.setMovable(False)
            graph.plot(range(obj["range"][0], obj["range"][1]),
                       graphPoints[obj["range"][0]:obj["range"][1]])
            label = QtWidgets.QLabel(
                f'peak_position: {obj["peak_position"]}\nrise_time: {obj["rise_time"]} decay_time: {obj["decay_time"]}\npeak_flux: {obj["peak_flux"]} duration: {obj["duration"]}')
            label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            widget = QtWidgets.QFrame(self.GraphArea)
            widget.setLayout(QtWidgets.QVBoxLayout(widget))
            widget.setFrameShape(QtWidgets.QFrame.NoFrame)
            widget.layout().addWidget(graph)
            widget.layout().addWidget(label, 0, QtCore.Qt.AlignBottom)
            self.GraphArea.addWidget(widget)
            i += 1
        plotmenu = PLotMenu(name, self.index, subplots=subplotnames)
        self.updatePlot(self.index)
        self.index += i
        plotmenu.plotSelected.connect(self.updatePlot)
        self.Menu.layout().addWidget(plotmenu)

    def updatePlot(self, index: int):
        self.GraphArea.setCurrentIndex(index)

    def fileDel(self, fileName: str):
        if fileName in self.OpenFiles:
            self.OpenFiles.remove(fileName)
        

    def addMenuOption(self, plotmenu: QtWidgets.QFrame):
        plotmenu.setParent(self.Menu)
        self.Menu.layout().addWidget(plotmenu, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)


class PLotMenu(QtWidgets.QFrame):
    plotSelected = QtCore.pyqtSignal(int)

    def __init__(self, name: str, index: int, subplots=[], parent=None):
        super(PLotMenu, self).__init__(parent=parent)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.HeaderFrame = QtWidgets.QFrame(parent=self)
        self.HeaderFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.HeaderFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.HeaderFrame.setLayout(QtWidgets.QHBoxLayout(self.HeaderFrame))
        self.HeaderFrame.layout().setContentsMargins(3, 3, 3, 3)
        mainPlot = QtWidgets.QToolButton(self.HeaderFrame)
        mainPlot.setText(name)
        mainPlot.setAutoRaise(True)
        mainPlot.clicked.connect(
            lambda state, x=index: self.plotSelected.emit(x))
        self.HeaderFrame.layout().addWidget(
            mainPlot, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        downArrow = QtWidgets.QToolButton(
            clicked=lambda: self.DownArrowAction())
        downArrow.setArrowType(QtCore.Qt.DownArrow)
        downArrow.setAutoRaise(True)
        effect = QtWidgets.QGraphicsDropShadowEffect(downArrow)
        effect.setBlurRadius(18)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setColor(QtGui.QColor(0, 0, 0, 100))
        downArrow.setGraphicsEffect(effect)
        self.HeaderFrame.layout().addWidget(downArrow, QtCore.Qt.AlignTop)

        self.SubPlotFrame = QtWidgets.QFrame(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.SubPlotFrame.sizePolicy().hasHeightForWidth())
        self.SubPlotFrame.setSizePolicy(sizePolicy)
        self.SubPlotFrame.setLayout(QtWidgets.QVBoxLayout(self.SubPlotFrame))
        self.SubPlotFrame.setContentsMargins(0, 0, 0, 0)
        self.SubPlotFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SubPlotFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SubPlotFrame.setVisible(False)

        i = index + 1
        for subplot in subplots:
            self.addSubPlot(subplot, i)
            i += 1

        self.layout().addWidget(self.HeaderFrame, QtCore.Qt.AlignTop)
        self.layout().addWidget(self.SubPlotFrame, QtCore.Qt.AlignTop)
        self.firstIndex = index
        self.lastIndex = i-1

    def addSubPlot(self, name: str, index: int):
        button = QtWidgets.QToolButton(self.SubPlotFrame)
        button.setAutoRaise(True)
        button.setText(name)
        button.clicked.connect(
            lambda state, x=index: self.plotSelected.emit(x))
        self.SubPlotFrame.layout().addWidget(button, 0, QtCore.Qt.AlignTop)

    def DownArrowAction(self):
        self.SubPlotFrame.setVisible(not self.SubPlotFrame.isVisible())


class MyButton(QtWidgets.QToolButton):
    def __init__(self, clickEvent, parent=None):
        super(MyButton, self).__init__(parent=parent, clicked=clickEvent)
        self.setAutoRaise(True)
        self.setMouseTracking(True)
        effect = QtWidgets.QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(18)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setColor(QtGui.QColor(255, 0, 0, 100))
        self.setGraphicsEffect(effect)
