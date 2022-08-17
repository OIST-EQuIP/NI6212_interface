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
        self.ni = NIDaqmx(dev_name)
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,'AI')
        self.tabs.addTab(self.tab2,'AO')
        self.tabs.addTab(self.tab3,'DO')
        self.createTab1()
        self.createTab2()
        self.createTab3()
        
        self.ch_status_value = QLabel("Crosshair: Outside plot")
        self.ch_x_value = QLabel("X: Unavailable")
        self.ch_y_value = QLabel("Y: Unavailable")
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.ch_status_value)
        self.hbox.addWidget(self.ch_x_value)
        self.hbox.addWidget(self.ch_y_value)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.layout.addLayout(self.hbox)
        
        Thread(target=self.plot_generator1, args=(self.AI_data_connector,)).start()
        Thread(target=self.plot_generator2, args=(self.data_connector2,)).start()
        Thread(target=self.plot_generator3, args=(self.data_connector3,)).start()
    
    
    def createTab1(self):
        self.tab1.layout = QVBoxLayout()
        self.AI_plot_running = False
        # Combo
        items = ['AI 0','AI 1','AI 2','AI 3','AI 4','AI 5','AI 6','AI 7']
        self.AI_channel_combo = self.createCombo(items)
        # Button
        self.AI_button = self.createButton('EXECUTE',True)
        self.AI_button.toggled.connect(self.slotAIButtonToggled)
        # Graph
        ## Create plot widget
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        plot_widget = LivePlotWidget(title="Analog Input", **kwargs)
        plot = LiveLinePlot()
        plot_widget.addItem(plot)
        ## Connect plot with DataConnector
        self.AI_data_connector = DataConnector(plot, max_points=200)
        self.AI_data_connector.pause()
        ## Connect moved and out signals with respective functions
        plot_widget.sig_crosshair_moved.connect(self.crosshair_moved)
        plot_widget.sig_crosshair_out.connect(self.crosshair_out)
        plot_widget.sig_crosshair_in.connect(self.crosshair_in)
        # Box layout
        ## HBox
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.AI_channel_combo)
        hbox.addWidget(self.AI_button)
        ## VBox
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(plot_widget)
        vbox.addLayout(hbox)
        
        self.tab1.setLayout(vbox)
    
    
    def createTab2(self):
        self.tab2.layout = QVBoxLayout()
        self.AO_plot_running = False
        ## TextBox
        self.textbox = QLineEdit(self)
        lim = QtCore.QRegExp("[0-9-.]+")
        self.textbox.setValidator(QtGui.QRegExpValidator(lim))
        ## Label
        label = QLabel("V",self)
        self.message = QLabel('',self)
        ## Combo
        items = ['AO 0','AO 1']
        self.AO_channel_combo = self.createCombo(items)
        ## Button
        self.AO_button = self.createButton('EXECUTE',True)
        self.AO_button.toggled.connect(self.slotAOButtonToggled)
        ## Graph
        ### Create plot widget
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        plot_widget = LivePlotWidget(title="Analog Output", **kwargs)
        plot = LiveLinePlot()
        plot_widget.addItem(plot)
        ### Connect plot with DataConnector
        self.data_connector2 = DataConnector(plot, max_points=200)
        self.data_connector2.pause()
        ### Connect moved and out signals with respective functions
        plot_widget.sig_crosshair_moved.connect(self.crosshair_moved)
        plot_widget.sig_crosshair_out.connect(self.crosshair_out)
        plot_widget.sig_crosshair_in.connect(self.crosshair_in)
        ## Box
        ### HBox
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.message)
        hbox.addWidget(self.textbox)
        hbox.addWidget(label)
        hbox.addWidget(self.AO_channel_combo)
        hbox.addWidget(self.AO_button)
        ### VBox
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(plot_widget)
        vbox.addLayout(hbox)
        self.tab2.setLayout(vbox)
    
    
    def createTab3(self):
        self.tab3.layout= QVBoxLayout()
        self.DO_plot_running = False
        self.DO_state = False
        # Combo
        items = ['Port 0','Port 1','Port 2']
        self.DO_port_combo = self.createCombo(items)
        items = ['PFI 0','PFI 1','PFI 2','PFI 3','PFI 4','PFI 5','PFI 6','PFI 7',]
        self.DO_channel_combo = self.createCombo(items)
        # Button
        self.DO_state_button = self.createButton('ON',True)
        self.DO_state_button.toggled.connect(self.slotDOStateButtonToggled)
        self.DO_button = self.createButton('EXECUTE',True)
        self.DO_button.toggled.connect(self.slotDOButtonToggled)
        # Graph
        ### Create plot widget
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        plot_widget = LivePlotWidget(title="Digital Output", **kwargs)
        plot = LiveLinePlot()
        plot_widget.addItem(plot)
        ### Connect plot with DataConnector
        self.data_connector3 = DataConnector(plot, max_points=200)
        self.data_connector3.pause()
        ### Connect moved and out signals with respective functions
        plot_widget.sig_crosshair_moved.connect(self.crosshair_moved)
        plot_widget.sig_crosshair_out.connect(self.crosshair_out)
        plot_widget.sig_crosshair_in.connect(self.crosshair_in)
        # Box layout
        ## HBox
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.DO_port_combo)
        hbox.addWidget(self.DO_channel_combo)
        hbox.addWidget(self.DO_state_button)
        hbox.addWidget(self.DO_button)
        ## VBox
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(plot_widget)
        vbox.addLayout(hbox)
        
        self.tab3.setLayout(vbox)
        
        
    
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
    
            
    def slotDOStateButtonToggled(self,checked):
        if checked:
            self.DO_state = True
            self.DO_state_button.setText('OFF')
        else:
            self.DO_state = False
            self.DO_state_button.setText('ON')
            
    
    def slotDOButtonToggled(self,checked):
        if checked:
            self.data_connector3.resume()
            self.DO_plot_running = True
            self.DO_button.setText('STOP')
        else:
            self.data_connector3.pause()
            self.DO_plot_running = False
            self.DO_button.setText('EXECUTE')
        
            
    def plot_generator1(self,*data_connectors):
        x = 0
        while True:
            for data_connector in data_connectors:
                if self.AI_plot_running == True:
                    channel = 'ai' + self.AI_channel_combo.currentText()[-1]
                    value = self.ni.getAIData(channel)
                    data_connector.cb_append_data_point(value[0],x)
                    x += 1
                
            sleep(0.02)
        
            
    def plot_generator2(self,*data_connectors):
        x = 0
        while True:
            value = self.textbox.text()
            
            if value == "" or value == "-" or value == ".":
                self.message.setText('')
                value = 0.0
            elif float(value) >= 10.0:
                self.message.setText('WARNING! : Set the value between -10 and 10')
                value = 10.0
            elif float(value) <= -10.0:
                self.message.setText('WARNING! : Set the value between -10 and 10')
                value = -10.0
            else:
                self.message.setText('')
                value = float(value)
                
            for data_connector in data_connectors:
                if self.AO_plot_running == True: 
                    channel = 'ao' + self.AO_channel_combo.currentText()[-1]
                    self.ni.setAOData(channel,value)
                    data_connector.cb_append_data_point(value,x)
                    x += 1
                
            sleep(0.02)
            
            
    def plot_generator3(self,*data_connectors):
        x = 0
        while True: 
            for data_connector in data_connectors:
                if self.DO_plot_running == True: 
                    port = 'port' + self.DO_port_combo.currentText()[-1]
                    channel = 'line' + self.DO_channel_combo.currentText()[-1]
                    self.ni.setDOData(port,channel,self.DO_state)
                    data_connector.cb_append_data_point(self.DO_state,x)
                    x += 1
                
            sleep(0.02)
    