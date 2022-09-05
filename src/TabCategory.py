from cgitb import text
from PyQt5.QtWidgets import QPushButton, QWidget, QTabWidget, QVBoxLayout, QLineEdit, QComboBox, QLabel, QCheckBox, QHBoxLayout
from PyQt5 import QtCore,QtGui

import pyqtgraph as pg

from pglive.kwargs import Crosshair
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

import numpy as np

from time import sleep

from NIDaqmxController import NIDaqmxController

from typing import Tuple

class TabCategory:
    def __init__(self, name: str, ni: NIDaqmxController, state: QLabel, x: QLabel, y: QLabel):
        self.tab = QVBoxLayout()
        self.hbox_main = QHBoxLayout()
        self.hbox_main.addStretch(1)
        self.vbox_main = QVBoxLayout()
        self.vbox_main.addStretch(1)
        self.plot_running = False
        self.np = np
        self.sleep = sleep
        self.checked = QtCore.Qt.Checked
        
        self.crosshair_moved_message = []
        self.crosshair_out_message = []
        self.crosshair_in_message = []
        
        self.ni = ni
        self.ch_status_value = state
        self.ch_x_value = x
        self.ch_y_value = y
        
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        self.plot_widget = LivePlotWidget(title=name, **kwargs)
        plot = LiveLinePlot()
        self.plot_widget.addItem(plot)
        ## Connect plot with DataConnector
        self.data_connector = DataConnector(plot, max_points=200)
        self.data_connector.pause()
        ## Connect moved and out signals with respective functions
        self.plot_widget.sig_crosshair_moved.connect(self.crosshair_moved)
        self.plot_widget.sig_crosshair_out.connect(self.crosshair_out)
        self.plot_widget.sig_crosshair_in.connect(self.crosshair_in)
    
    
    def getLayout(self) -> QVBoxLayout:
        return self.tab

    
    def createCombo(self, items: list) -> QComboBox:
        combo = QComboBox()
        for item in items:
            combo.addItem(item)
            
        return combo
    
    
    def createButton(self, label: str, toggled: bool) -> QPushButton:
        button = QPushButton(label)
        button.setCheckable(toggled)
        return button
    
    
    def createTextBox(self, limit: str, width: int = 100) -> QLineEdit:
        textbox = QLineEdit()
        lim = QtCore.QRegExp(limit)
        textbox.setValidator(QtGui.QRegExpValidator(lim))
        textbox.setFixedWidth(width)
        return textbox
    
    
    def createLabel(self, value: str) -> QLabel:
        label = QLabel(value)
        return label
    
    
    def createCheckbox(self) -> QCheckBox:
        checkbox = QCheckBox()
        return checkbox
    
    
    def createCheckboxLayout(self, r: int) -> Tuple[list, QHBoxLayout]:
        checkboxs = list()
        labels = list()
        vboxs = list()
        for i in range(r):
            checkboxs.append(QCheckBox())
            labels.append(QLabel(str(i)))
            labels[i].setAlignment(QtCore.Qt.AlignCenter)
            vboxs.append(QVBoxLayout())
            vboxs[i].addWidget(checkboxs[i])
            vboxs[i].addWidget(labels[i])
            
        checkbox_layout = QHBoxLayout()
        for i in vboxs:
            checkbox_layout.addLayout(i) 
            
        return checkboxs,checkbox_layout   
            
    
    def crosshair_moved(self, crosshair_pos: QtCore.QPointF) -> None:
        self.ch_x_value.setText(f"X: {crosshair_pos.x()}")
        self.ch_y_value.setText(f"Y: {crosshair_pos.y()}")


    def crosshair_out(self) -> None:
        self.ch_status_value.setText("Crosshair: Outside plot")
        self.ch_x_value.setText(f"X: Unavailable")
        self.ch_y_value.setText(f"Y: Unavailable")


    def crosshair_in(self) -> None:
        self.ch_status_value.setText("Crosshair: Inside plot")
        