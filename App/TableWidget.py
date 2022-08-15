from PyQt5.QtWidgets import QApplication,QPushButton, QWidget, QTabWidget, QVBoxLayout, QLineEdit, QComboBox, QLabel, QHBoxLayout
from PyQt5 import QtCore
import sys
import pglive.examples_pyqt5 as examples
import signal
from threading import Thread

import pyqtgraph as pg

from time import sleep

from pglive.kwargs import Crosshair
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveScatterPlot
from pglive.sources.live_plot_widget import LivePlotWidget

import numpy as np
from NIDaqmx import NIDaqmx

class TableWidget(QWidget):
    def __init__(self,parent):
        super(QWidget,self).__init__(parent)
        self.plot_running1 = False
        self.plot_running2 = False      
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,'AI')
        self.tabs.addTab(self.tab2,'AO')
        
        # Create first tab
        self.tab1.layout = QVBoxLayout()
        ## Combo
        self.combo1 = QComboBox(self)
        self.combo1.addItem('ai0')
        self.combo1.addItem('ai1')
        self.combo1.addItem('ai2')
        self.combo1.addItem('ai3')
        self.combo1.addItem('ai4')
        self.combo1.addItem('ai5')
        self.combo1.addItem('ai6')
        self.combo1.addItem('ai7')
        ## Button
        self.button1 = QPushButton('EXECUTE')
        self.button1.setCheckable(True)
        self.button1.toggled.connect(self.slot_button1_toggled)
        ## Graph
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        ### Create plot widget
        plot_widget1 = LivePlotWidget(title="Line Plot and Crosshair @ 100Hz", **kwargs)
        plot1 = LiveScatterPlot()
        plot_widget1.addItem(plot1)
        ### Connect plot with DataConnector
        self.data_connector1 = DataConnector(plot1, max_points=1000)
        self.data_connector1.pause()
        ### Create crosshair X, Y label
        self.ch_status_value = QLabel("Crosshair: Outside plot")
        self.ch_x_value = QLabel("X: Unavailable")
        self.ch_y_value = QLabel("Y: Unavailable")
        ### Connect moved and out signals with respective functions
        plot_widget1.sig_crosshair_moved.connect(self.crosshair_moved)
        plot_widget1.sig_crosshair_out.connect(self.crosshair_out)
        plot_widget1.sig_crosshair_in.connect(self.crosshair_in)
        ## Box
        ### HBox
        self.hbox1 = QHBoxLayout()
        self.hbox1.addStretch(1)
        self.hbox1.addWidget(self.ch_status_value)
        self.hbox1.addWidget(self.ch_x_value)
        self.hbox1.addWidget(self.ch_y_value)
        self.hbox1.addWidget(self.combo1)
        self.hbox1.addWidget(self.button1)
        ### VBox
        self.vbox1 = QVBoxLayout()
        self.vbox1.addStretch(1)
        self.vbox1.addWidget(plot_widget1)
        self.vbox1.addLayout(self.hbox1)
        
        self.tab1.setLayout(self.vbox1)
        
        # Criate Second tab
        self.tab2.layout = QVBoxLayout()
        ## TextBox
        self.textbox2 = QLineEdit(self)
        ## Label
        self.label2 = QLabel("V",self)
        ## Combo
        self.combo2 = QComboBox(self)
        self.combo2.addItem("ao0")
        self.combo2.addItem("ao1")
        ## Button
        self.button2 = QPushButton('EXECUTE')
        self.button2.setCheckable(True)
        self.button2.toggled.connect(self.slot_button2_toggled)
        ## graph
        ## Graph
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        ### Create plot widget
        plot_widget2 = LivePlotWidget(title="Line Plot and Crosshair @ 100Hz", **kwargs)
        plot2 = LiveScatterPlot()
        plot_widget2.addItem(plot2)
        ### Connect plot with DataConnector
        self.data_connector2 = DataConnector(plot2, max_points=1000)
        self.data_connector2.pause()
        ### Create crosshair X, Y label
        self.ch_status_value = QLabel("Crosshair: Outside plot")
        self.ch_x_value = QLabel("X: Unavailable")
        self.ch_y_value = QLabel("Y: Unavailable")
        ### Connect moved and out signals with respective functions
        plot_widget2.sig_crosshair_moved.connect(self.crosshair_moved)
        plot_widget2.sig_crosshair_out.connect(self.crosshair_out)
        plot_widget2.sig_crosshair_in.connect(self.crosshair_in)
        ## Box
        ### HBox
        self.hbox2 = QHBoxLayout()
        self.hbox2.addStretch(1)
        self.hbox2.addWidget(self.ch_status_value)
        self.hbox2.addWidget(self.ch_x_value)
        self.hbox2.addWidget(self.ch_y_value)
        self.hbox2.addWidget(self.textbox2)
        self.hbox2.addWidget(self.label2)
        self.hbox2.addWidget(self.combo2)
        self.hbox2.addWidget(self.button2)
        ### VBox
        self.vbox2 = QVBoxLayout()
        self.vbox2.addStretch(1)
        self.vbox2.addWidget(plot_widget2)
        self.vbox2.addLayout(self.hbox2)
        self.tab2.setLayout(self.vbox2)
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        
        # Thread(target=self.plot_generator1, args=(self.data_connector1,)).start()
        # Thread(target=self.plot_generator2, args=(self.data_connector2,)).start()
        # signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
        
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
        
        
    def slot_button1_toggled(self,checked):
        if checked:
            self.data_connector1.resume()
            self.plot_running1 = True
            self.button1.setText('STOP')
        else:
            self.data_connector1.pause()
            self.plot_running1 = False
            self.button1.setText('EXECUTE')
            
    
    def slot_button2_toggled(self,checked):
        if checked:
            self.data_connector2.resume()
            self.plot_running2 = True
            self.button2.setText('STOP')
        else:
            self.data_connector2.pause()
            self.plot_running2 = False
            self.button2.setText('EXECUTE')
        
            
    def plot_generator1(self,*data_connectors):
        x = 0
        while self.plot_running1:
            if self.plot_running1 != False: x += 1
            print(x)
            
            for data_connector in data_connectors:
                data_connector.cb_append_data_point(1,x)
                
            sleep(0.01)
            
    def plot_generator2(self,*data_connectors):
        y = 0
        while self.plot_running2:
            if self.plot_running2 != False: y += 1
            print(y)
            
            for data_connector in data_connectors:
                data_connector.cb_append_data_point(1,y)
                
            sleep(0.01)
