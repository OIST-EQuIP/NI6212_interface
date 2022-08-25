from PyQt5.QtWidgets import QPushButton, QWidget, QTabWidget, QVBoxLayout, QLineEdit, QComboBox, QLabel, QCheckBox, QHBoxLayout
from PyQt5 import QtCore,QtGui
from threading import Thread

import pyqtgraph as pg

from pglive.kwargs import Crosshair
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

from time import sleep

import numpy as np

from NIDaqmx import NIDaqmx

class TableWidget(QWidget):
    def __init__(self,parent) -> None:
        super(QWidget,self).__init__(parent)
        self.ni = NIDaqmx()
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,'AI')
        self.tabs.addTab(self.tab2,'AO')
        self.tabs.addTab(self.tab3,'DO')
        self.tabs.addTab(self.tab4,'Scan Amplitude')
        self.createTab1()
        self.createTab2()
        self.createTab3()
        self.createTab4()
        
        
        label = QLabel("Device Name")
        label.setFixedWidth(80)
        self.dev_name = QLineEdit(self)
        self.dev_name.setFixedWidth(150)
        self.dev_name.setText("Dev1")
        self.dev_name.setEnabled(False)
        self.ni.setDevName(self.dev_name.text())
        
        self.editButton = self.createButton('Edit',True)
        self.editButton.setFixedWidth(100)
        self.editButton.toggled.connect(self.slotEditButtonToggled)
        
        self.ch_status_value = QLabel("Crosshair: Outside plot")
        self.ch_x_value = QLabel("X: Unavailable")
        self.ch_y_value = QLabel("Y: Unavailable")
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(label)
        self.hbox.addWidget(self.dev_name)
        self.hbox.addWidget(self.editButton)
        self.hbox.addWidget(self.ch_status_value)
        self.hbox.addWidget(self.ch_x_value)
        self.hbox.addWidget(self.ch_y_value)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.layout.addLayout(self.hbox)
        
        Thread(target=self.plotGenerator1, args=(self.AI_data_connector,)).start()
        Thread(target=self.plotGenerator2, args=(self.AO_data_connector,)).start()
        Thread(target=self.plotGenerator3, args=(self.DO_data_connector,)).start()
        Thread(target=self.plotGenerator4, args=(self.SA_data_connector,)).start()
    
    
    # Create AI tab
    def createTab1(self) -> None:
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
    
    
    # Create AO tab
    def createTab2(self) -> None:
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
        self.AO_data_connector = DataConnector(plot, max_points=200)
        self.AO_data_connector.pause()
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
    
    
    # Create DO tab
    def createTab3(self) -> None:
        self.tab3.layout= QVBoxLayout()
        self.DO_plot_running = False
        self.DO_state = False
        # Combo
        items = ['Port 0','Port 1','Port 2']
        self.DO_port_combo = self.createCombo(items)
        self.DO_port_combo.setCurrentIndex(1)
        # Checkbox
        self.checkboxs = list()
        self.labels = list()
        vboxs = list()
        for i in range(8):
            self.checkboxs.append(QCheckBox())
            self.labels.append(QLabel(str(i)))
            self.labels[i].setAlignment(QtCore.Qt.AlignCenter)
            vboxs.append(QVBoxLayout())
            vboxs[i].addWidget(self.checkboxs[i])
            vboxs[i].addWidget(self.labels[i])
            
        checkbox_hbox = QHBoxLayout()
        for i in vboxs:
            checkbox_hbox.addLayout(i)    

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
        self.DO_data_connector = DataConnector(plot, max_points=200)
        self.DO_data_connector.pause()
        ### Connect moved and out signals with respective functions
        plot_widget.sig_crosshair_moved.connect(self.crosshair_moved)
        plot_widget.sig_crosshair_out.connect(self.crosshair_out)
        plot_widget.sig_crosshair_in.connect(self.crosshair_in)
        # Box layout
        ## HBox
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.DO_port_combo)
        hbox.addLayout(checkbox_hbox)
        hbox.addWidget(self.DO_state_button)
        hbox.addWidget(self.DO_button)
        ## VBox
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(plot_widget)
        vbox.addLayout(hbox)
        
        self.tab3.setLayout(vbox)
    
    
    # Create Scan Amplitude tab
    def createTab4(self) -> None:
        self.tab4.layout= QVBoxLayout()
        self.SA_plot_running = False
        self.SA_scan_state = False
        # Label
        self.system_message = QLabel('')
        threshold_label = QLabel('Threshold')
        vmax_label = QLabel('vmax')
        vmin_label = QLabel('vmin')
        vamp_label = QLabel('vamp')
        step_label = QLabel('step size')
        AO_label = QLabel('AO Channel')
        AI_label = QLabel('AI Channel')
        # TextBox
        lim = QtCore.QRegExp("[0-9-.]+")
        self.threshold = QLineEdit(self)
        self.threshold.setFixedWidth(120)
        self.threshold.setValidator(QtGui.QRegExpValidator(lim))
        self.vmax = QLineEdit(self)
        self.vmax.setFixedWidth(120)
        self.vmax.setValidator(QtGui.QRegExpValidator(lim))
        self.vmax.setText("5.4")
        self.vmax.setEnabled(False)
        self.vmin = QLineEdit(self)
        self.vmin.setFixedWidth(120)
        self.vmin.setValidator(QtGui.QRegExpValidator(lim))
        self.vmin.setText("-5.4")
        self.vmin.setEnabled(False)
        self.vamp = QLineEdit(self)
        self.vamp.setFixedWidth(120)
        self.vamp.setValidator(QtGui.QRegExpValidator(lim))
        self.vamp.setText("")
        self.vamp.setEnabled(True)
        self.step = QLineEdit(self)
        self.step.setFixedWidth(120)
        self.step.setValidator(QtGui.QRegExpValidator(lim))
        # Button
        self.load_button = self.createButton('LOAD',True)
        self.load_button.toggled.connect(self.slotSALoadButtonToggled)
        self.scan_button = self.createButton('SCAN',True)
        self.scan_button.toggled.connect(self.slotSAScanButtonToggled)
        # Combo
        items = ['AO 0','AO 1']
        self.AO_channel_combo = self.createCombo(items)
        items = ['AI 0','AI 1','AI 2','AI 3','AI 4','AI 5','AI 6','AI 7']
        self.AI_channel_combo = self.createCombo(items)
        # Graph
        ### Create plot widget
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        plot_widget = LivePlotWidget(title="", **kwargs)
        plot = LiveLinePlot()
        plot_widget.addItem(plot)
        ### Connect plot with DataConnector
        self.SA_data_connector = DataConnector(plot, max_points=200)
        self.SA_data_connector.pause()
        ### Connect moved and out signals with respective functions
        plot_widget.sig_crosshair_moved.connect(self.crosshair_moved)
        plot_widget.sig_crosshair_out.connect(self.crosshair_out)
        plot_widget.sig_crosshair_in.connect(self.crosshair_in)
        # Box layout
        hbox1 = QHBoxLayout()
        hbox1.addWidget(threshold_label)
        hbox1.addWidget(self.threshold)
        hbox1.addWidget(QLabel('V'))
        hbox2 = QHBoxLayout()
        hbox2.addWidget(vmax_label)
        hbox2.addWidget(self.vmax)
        hbox2.addWidget(QLabel('V'))
        hbox3 = QHBoxLayout()
        hbox3.addWidget(vmin_label)
        hbox3.addWidget(self.vmin)
        hbox3.addWidget(QLabel('V'))
        hbox4 = QHBoxLayout()
        hbox4.addWidget(vamp_label)
        hbox4.addWidget(self.vamp)
        hbox4.addWidget(QLabel('V'))
        hbox5 = QHBoxLayout()
        hbox5.addWidget(step_label)
        hbox5.addWidget(self.step)
        hbox5.addWidget(QLabel('V'))
        hbox6 = QHBoxLayout()
        hbox6.addWidget(AO_label)
        hbox6.addWidget(self.AO_channel_combo)
        hbox6.addWidget(AI_label)
        hbox6.addWidget(self.AI_channel_combo)
        hbox7 = QHBoxLayout()
        hbox7.addWidget(self.load_button)
        hbox7.addWidget(self.scan_button)
        
        ## Main VBox
        vbox_main = QVBoxLayout()
        vbox_main.addStretch(1)
        vbox_main.addWidget(self.system_message)
        vbox_main.addLayout(hbox1)
        vbox_main.addLayout(hbox2)
        vbox_main.addLayout(hbox3)
        vbox_main.addLayout(hbox4)
        vbox_main.addLayout(hbox5)
        vbox_main.addLayout(hbox6)
        vbox_main.addLayout(hbox7)
        
        ## Main HBox
        hbox_main = QHBoxLayout()
        hbox_main.addStretch(1)
        hbox_main.addWidget(plot_widget)
        hbox_main.addLayout(vbox_main)
        
        self.tab4.setLayout(hbox_main)
    
    
    def createCombo(self,items: list) -> QComboBox:
        combo = QComboBox(self)
        for item in items:
            combo.addItem(item)
            
        return combo
    
    
    def createButton(self,label: str,toggled: bool) -> QPushButton:
        button = QPushButton(label)
        button.setCheckable(toggled)
        return button
    
    
    def crosshair_moved(self,crosshair_pos: QtCore.QPointF) -> None:
        """Update crosshair X, Y label when crosshair move"""
        self.ch_x_value.setText(f"X: {crosshair_pos.x()}")
        self.ch_y_value.setText(f"Y: {crosshair_pos.y()}")


    def crosshair_out(self) -> None:
        """Update crosshair X, Y label when crosshair leaves plot area"""
        self.ch_status_value.setText("Crosshair: Outside plot")
        self.ch_x_value.setText(f"X: Unavailable")
        self.ch_y_value.setText(f"Y: Unavailable")


    def crosshair_in(self) -> None:
        """Update crosshair X, Y label when crosshair enters plot area"""
        self.ch_status_value.setText("Crosshair: Inside plot")
    
    
    def slotEditButtonToggled(self,checked: bool) -> None:
        if checked:
            self.editButton.setText("Set")
            self.dev_name.setEnabled(True)
        else:
            self.editButton.setText("Edit")
            self.ni.setDevName(self.dev_name.text())
            self.dev_name.setEnabled(False)
        
        
    def slotAIButtonToggled(self,checked: bool) -> None:
        if checked:
            self.AI_data_connector.resume()
            self.AI_plot_running = True
            self.AI_button.setText('STOP')
        else:
            self.AI_data_connector.pause()
            self.AI_plot_running = False
            self.AI_button.setText('EXECUTE')
            
    
    def slotAOButtonToggled(self,checked: bool) -> None:
        if checked:
            self.AO_data_connector.resume()
            self.AO_plot_running = True
            self.AO_button.setText('STOP')
        else:
            self.AO_data_connector.pause()
            self.AO_plot_running = False
            self.AO_button.setText('EXECUTE')
    
            
    def slotDOStateButtonToggled(self,checked: bool) -> None:
        if checked:
            self.DO_state = True
            self.DO_state_button.setText('OFF')
        else:
            self.DO_state = False
            self.DO_state_button.setText('ON')
            
    
    def slotDOButtonToggled(self,checked: bool) -> None:
        if checked:
            self.DO_data_connector.resume()
            self.DO_plot_running = True
            self.DO_button.setText('STOP')
        else:
            self.DO_data_connector.pause()
            self.DO_plot_running = False
            self.DO_button.setText('EXECUTE')
        
    
    def slotSALoadButtonToggled(self,checked: bool) -> None:
        if checked:
            self.SA_data_connector.resume()
            self.SA_plot_running = True
            self.scan_button.setEnabled(True)
            self.load_button.setText('STOP')
        else:
            self.SA_data_connector.pause()
            self.SA_plot_running = False
            self.scan_button.setEnabled(False)
            self.load_button.setText('LOAD')
        
        
    def slotSAScanButtonToggled(self,checked: bool) -> None:
        if checked:
            self.SA_scan_state = True
            self.scan_button.setText('STOP')
        else:
            self.SA_scan_state = False
            self.scan_button.setText('SCAN')
    
            
    def plotGenerator1(self,*data_connectors: tuple) -> None:
        x = 0
        while True:
            for data_connector in data_connectors:
                if self.AI_plot_running == True:
                    channel = 'ai' + self.AI_channel_combo.currentText()[-1]
                    value = self.ni.getAIData(channel)
                    data_connector.cb_append_data_point(value[0],x)
                    x += 1
                
            sleep(0.02)
        
            
    def plotGenerator2(self,*data_connectors: tuple) -> None:
        x = 0
        while True:
            value = self.textbox.text()
            
            if value == "" or value == "-" or value == ".":
                self.message.setText('')
                value = 0.0
            elif float(value) > 10.0:
                self.message.setText('WARNING! : Set the value between -10.0 and 10.0')
                value = 10.0
            elif float(value) < -10.0:
                self.message.setText('WARNING! : Set the value between -10.0 and 10.0')
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
            
            
    def plotGenerator3(self,*data_connectors: tuple) -> None:
        x = 0
        while True: 
            for data_connector in data_connectors:
                if self.DO_plot_running == True: 
                    port = 'port' + self.DO_port_combo.currentText()[-1]
                    select = list()
                    status = list()
                    channels = list()
                    for i in range(len(self.checkboxs)):
                        if self.checkboxs[i].checkState() == QtCore.Qt.Checked:
                            select.append(i)
                            status.append(self.DO_state)

                    for i in select:
                        channels.append(f'line{i}')
                    self.ni.setDOData(port,channels,status)
                    data_connector.cb_append_data_point(self.DO_state,x)
                    x += 1
                
            sleep(0.02)
    
    
    def plotGenerator4(self,*data_connectors: tuple) -> None:
        x = 0
        AO_value = 0
        state = True
        while True:
            for data_connector in data_connectors:
                if self.SA_plot_running == True:
                    threshold = float(self.threshold.text()) if self.threshold.text() != '' and self.threshold.text() != '-' else 0.0
                    vmax = float(self.vmax.text()) if self.vmax.text() != '' and self.vmax.text() != '-' else 0.0
                    vmin = float(self.vmin.text()) if self.vmin.text() != '' and self.vmin.text() != '-' else 0.0
                    vamp = float(self.vamp.text()) if self.vamp.text() != '' and self.vamp.text() != '-' else 0.0
                    step = float(self.step.text()) if self.step.text() != '' and self.step.text() != '-' else 0.0
                    AI_channel = 'ai' + self.AI_channel_combo.currentText()[-1]
                    # AI_value = round(self.ni.getAIData(AI_channel)[0],int(str(threshold).split('.')[1])+1)
                    AI_value = self.ni.getAIData(AI_channel)[0]
                    AO_channel = 'ao' + self.AO_channel_combo.currentText()[-1]
                    AO_value,state = self.AOUpdateRate(vmax,vmin,vamp,step,AO_value,state)
                    self.ni.setAOData(AO_channel,AO_value)
                    # print(f'{threshold},{AI_value}')
                    # if self.SA_scan_state:
                    #     if threshold == AI_value:
                    #         self.system_message.setText(f'{x},{AI_value}')
                    #         print(1)
                    data_connector.cb_append_data_point(AI_value,x)
                    x += 1
                
            sleep(0.02)
            
            
    def AOUpdateRate(self,vmax: float,vmin: float,vamp: float,step: float,now_value: float,now_state: bool) -> float:        
        if now_state:
            result = now_value + step
            state = now_state if result < vmax and np.abs(result) < vamp else not(now_state)
        else:
            result = now_value - step 
            state = now_state if result > vmin and np.abs(result) < vamp else not(now_state)
        return result,state
    
    
    def ScanAmplitude(self) -> None:
        pass