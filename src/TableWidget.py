from PyQt5.QtWidgets import QPushButton, QWidget, QTabWidget, QVBoxLayout, QLineEdit, QComboBox, QLabel, QHBoxLayout
from PyQt5 import QtCore,QtGui
import pglive.examples_pyqt5 as examples
import signal
from threading import Thread

import pyqtgraph as pg

from time import sleep

from pglive.kwargs import Crosshair
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

from NIDaqmx import NIDaqmx

class TableWidget(QWidget):
    def __init__(self,parent):
        super(QWidget,self).__init__(parent)
        dev_name = "Dev2"
        self.AI_plot_running = False
        self.AO_plot_running = False
        self.ni = NIDaqmx(dev_name)
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,'AI')
        self.tabs.addTab(self.tab2,'AO')
        self.createTab1()
        self.createTab2()
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        
        Thread(target=self.plot_generator1, args=(self.AI_data_connector,)).start()
        Thread(target=self.plot_generator2, args=(self.data_connector2,)).start()   
        signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
    
    
    def createTab1(self):
        self.tab1.layout = QVBoxLayout()
        # Combo
        items = ['ai0','ai1','ai2','ai3','ai4','ai5','ai6','ai7']
        self.AI_combo = self.createCombo(items)
        # Button
        self.AI_button = self.createButton('EXECUTE',True)
        self.AI_button.toggled.connect(self.slotAIButtonToggled)
        # Graph
        ## Create plot widget
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        plot_widget = LivePlotWidget(title="Line Plot and Crosshair @ 100Hz", **kwargs)
        plot = LiveLinePlot()
        plot_widget.addItem(plot)
        ## Connect plot with DataConnector
        self.AI_data_connector = DataConnector(plot, max_points=200)
        self.AI_data_connector.pause()
        ### Create crosshair X, Y label
        self.ch_status_value = QLabel("Crosshair: Outside plot")
        self.ch_x_value = QLabel("X: Unavailable")
        self.ch_y_value = QLabel("Y: Unavailable")
        ## Connect moved and out signals with respective functions
        plot_widget.sig_crosshair_moved.connect(self.crosshair_moved)
        plot_widget.sig_crosshair_out.connect(self.crosshair_out)
        plot_widget.sig_crosshair_in.connect(self.crosshair_in)
        # Box layout
        ## HBox
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.ch_status_value)
        hbox.addWidget(self.ch_x_value)
        hbox.addWidget(self.ch_y_value)
        hbox.addWidget(self.AI_combo)
        hbox.addWidget(self.AI_button)
        ## VBox
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(plot_widget)
        vbox.addLayout(hbox)
        
        self.tab1.setLayout(vbox)
    
    
    def createTab2(self):
        # Criate Second tab
        self.tab2.layout = QVBoxLayout()
        ## TextBox
        self.textbox = QLineEdit(self)
        lim = QtCore.QRegExp("[0-9-.]+")
        self.textbox.setValidator(QtGui.QRegExpValidator(lim))
        ## Label
        label = QLabel("V",self)
        ## Combo
        items = ['ao0','ao1']
        self.AO_combo = self.createCombo(items)
        ## Button
        self.AO_button = self.createButton('EXECUTE',True)
        self.AO_button.toggled.connect(self.slotAOButtonToggled)
        ## Graph
        ### Create plot widget
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        plot_widget = LivePlotWidget(title="Line Plot and Crosshair @ 100Hz", **kwargs)
        plot = LiveLinePlot()
        plot_widget.addItem(plot)
        ### Connect plot with DataConnector
        self.data_connector2 = DataConnector(plot, max_points=200)
        self.data_connector2.pause()
        ### Create crosshair X, Y label
        self.ch_status_value = QLabel("Crosshair: Outside plot")
        self.ch_x_value = QLabel("X: Unavailable")
        self.ch_y_value = QLabel("Y: Unavailable")
        ### Connect moved and out signals with respective functions
        plot_widget.sig_crosshair_moved.connect(self.crosshair_moved)
        plot_widget.sig_crosshair_out.connect(self.crosshair_out)
        plot_widget.sig_crosshair_in.connect(self.crosshair_in)
        ## Box
        ### HBox
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.ch_status_value)
        hbox.addWidget(self.ch_x_value)
        hbox.addWidget(self.ch_y_value)
        hbox.addWidget(self.textbox)
        hbox.addWidget(label)
        hbox.addWidget(self.AO_combo)
        hbox.addWidget(self.AO_button)
        ### VBox
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(plot_widget)
        vbox.addLayout(hbox)
        self.tab2.setLayout(vbox)
        
    
    def createCombo(self,items: list) -> QComboBox:
        combo = QComboBox(self)
        for item in items:
            combo.addItem(item)
            
        return combo
    
    
    def createButton(self,label: str,toggled: bool) -> QPushButton:
        button = QPushButton(label)
        button.setCheckable(toggled)
        return button
    
    
    def crosshair_moved(self,crosshair_pos: QtCore.QPointF):
        """Update crosshair X, Y label when crosshair move"""
        self.ch_x_value.setText(f"X: {crosshair_pos.x()}")
        self.ch_y_value.setText(f"Y: {crosshair_pos.y()}")


    def crosshair_out(self):
        """Update crosshair X, Y label when crosshair leaves plot area"""
        self.ch_status_value.setText("Crosshair: Outside plot")
        self.ch_x_value.setText(f"X: Unavailable")
        self.ch_y_value.setText(f"Y: Unavailable")


    def crosshair_in(self):
        """Update crosshair X, Y label when crosshair enters plot area"""
        self.ch_status_value.setText("Crosshair: Inside plot")
        
        
    def slotAIButtonToggled(self,checked):
        if checked:
            self.AI_data_connector.resume()
            self.AI_plot_running = True
            self.AI_button.setText('STOP')
        else:
            self.AI_data_connector.pause()
            self.AI_plot_running = False
            self.AI_button.setText('EXECUTE')
            
    
    def slotAOButtonToggled(self,checked):
        if checked:
            self.data_connector2.resume()
            self.AO_plot_running = True
            self.AO_button.setText('STOP')
        else:
            self.data_connector2.pause()
            self.AO_plot_running = False
            self.AO_button.setText('EXECUTE')
        
            
    def plot_generator1(self,*data_connectors):
        x = 0
        while True:
            if self.AI_plot_running != False: x += 1
            value = self.ni.getInputData(self.AI_combo.currentText())
            for data_connector in data_connectors:
                data_connector.cb_append_data_point(value[0],x)
                
            sleep(0.02)
        
            
    def plot_generator2(self,*data_connectors):
        y = 0
        while True:
            if self.AO_plot_running != False: y += 1
            value = self.textbox.text()
            if value == "" or value == "-" or value == ".":
                value = 0.0
            elif float(value) >= 10.0:
                value = 10.0
            elif float(value) <= -10.0:
                value = -10.0
            else:
                value = float(value)
                
            for data_connector in data_connectors:
                self.ni.setOutputData(self.AO_combo.currentText(),value)
                data_connector.cb_append_data_point(value,y)
                
            sleep(0.02)
    