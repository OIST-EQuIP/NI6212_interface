from PyQt5.QtWidgets import QLabel,QHBoxLayout

from TabCategory import TabCategory
from NIDAQmxController import NIDAQ_ai_task
from NIDAQmxController import NIDAQ_ao_task
from NIDAQmxController import NIDAQ_do_task

import time

class ScanAmplitude(TabCategory):
    """
    Class that holds information on scan amplitude tabs.

    Args:
        TabCategory (_type_): Parent class.
    """
    def __init__(self, name: str, state: QLabel, x: QLabel, y: QLabel) -> None:
        """
        Constructor.

        Args:
            name (str): Plot Title.
            state (QLabel): Label to indicate whether the mouse cursor is in the plot area.
            x (QLabel): Label to display x-coordinates of the plot area selected by the mouse cursor.
            y (QLabel): Label to display y-coordinates of the plot area selected by the mouse cursor.
        """
        super().__init__(name,state,x,y)
        # Label
        self.system_message = self.createLabel('')
        # TextBox
        lim = "[0-9-.]+"
        self.threshold = self.createTextBox(lim,120)
        self.vmax = self.createTextBox(lim,120)
        self.vmax.setText("5.4")
        self.vmax.setEnabled(False)
        self.vmin = self.createTextBox(lim,120)
        self.vmin.setText("-5.4")
        self.vmin.setEnabled(False)
        self.vamp = self.createTextBox(lim,120)
        self.vamp.setText("5.0")
        self.vamp.setEnabled(True)
        self.step = self.createTextBox(lim,120)
        self.dt = self.createTextBox(lim,120)
        # Button
        self.scan_button = self.createButton('SCAN',True)
        self.scan_button.toggled.connect(self.slotScanButtonToggled)
        self.lock_button = self.createButton('LOCK',True)
        self.lock_button.toggled.connect(self.slotLockButtonToggled)
        self.lock_button.setEnabled(False)
        # Combo box
        ao_chan = ['ao0', 'ao1']
        self.AO_channel_combo = self.createCombo(ao_chan)
        self.ao_current_channel = self.AO_channel_combo.currentIndex()
        ai_chan = ['ai0','ai1','ai2','ai3','ai4','ai5','ai6','ai7']
        self.AI_channel_combo = self.createCombo(ai_chan)
        self.ai_current_channel = self.AI_channel_combo.currentIndex()
        port = ['port0', 'port1', 'port2']
        self.DO_port_combo = self.createCombo(port)
        self.DO_port_combo.setCurrentIndex(1)
        self.do_current_port = self.DO_port_combo.currentIndex()
        line = ['line0', 'line1', 'line2', 'line3', 'line4', 'line5', 'line6', 'line7']
        self.DO_channel_combo = self.createCombo(line)
        self.do_current_channel = self.DO_channel_combo.currentIndex()
        # Box layout
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.createLabel('Threshold'))
        hbox1.addWidget(self.threshold)
        hbox1.addWidget(self.createLabel('V'))
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.createLabel('vmax'))
        hbox2.addWidget(self.vmax)
        hbox2.addWidget(self.createLabel('V'))
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.createLabel('vmin'))
        hbox3.addWidget(self.vmin)
        hbox3.addWidget(self.createLabel('V'))
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.createLabel('vamp'))
        hbox4.addWidget(self.vamp)
        hbox4.addWidget(self.createLabel('V'))
        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.createLabel('step size'))
        hbox5.addWidget(self.step)
        hbox5.addWidget(self.createLabel('V'))
        hbox6 = QHBoxLayout()
        hbox6.addWidget(self.createLabel('dt'))
        hbox6.addWidget(self.dt)
        hbox6.addWidget(self.createLabel('ms'))
        hbox7 = QHBoxLayout()
        hbox7.addWidget(self.createLabel('AO Channel'))
        hbox7.addWidget(self.AO_channel_combo)
        hbox7.addWidget(self.createLabel('AI Channel'))
        hbox7.addWidget(self.AI_channel_combo)
        hbox8 = QHBoxLayout()
        hbox8.addWidget(self.createLabel('DO Port/Channel'))
        hbox8.addWidget(self.DO_port_combo)
        hbox8.addWidget(self.DO_channel_combo)
        hbox9 = QHBoxLayout()
        hbox9.addWidget(self.scan_button)
        hbox9.addWidget(self.lock_button)
        
        ## Main VBox
        self.vbox_main.addWidget(self.system_message)
        self.vbox_main.addLayout(hbox1)
        self.vbox_main.addLayout(hbox2)
        self.vbox_main.addLayout(hbox3)
        self.vbox_main.addLayout(hbox4)
        self.vbox_main.addLayout(hbox5)
        self.vbox_main.addLayout(hbox6)
        self.vbox_main.addLayout(hbox7)
        self.vbox_main.addLayout(hbox8)
        self.vbox_main.addLayout(hbox9)
        
        ## Main HBox
        self.hbox_main.addWidget(self.plot_widget)
        self.hbox_main.addLayout(self.vbox_main)
        
        self.tab.addLayout(self.hbox_main)
        
        self.ai_task = NIDAQ_ai_task('Dev1',self.AI_channel_combo.currentText())
        self.ao_task = NIDAQ_ao_task('Dev1',self.AO_channel_combo.currentText())
        self.do_task = NIDAQ_do_task('Dev1',self.DO_port_combo.currentText(),self.DO_channel_combo.currentText())
        
    
    def slotScanButtonToggled(self, checked: bool) -> None:
        """
        A function that defines the behavior of a scan button.
        When the button is pressed, the combo boxes and text boxes are disabled and the plotting begins.
        When the button is released, it stops the plot and activates the combo boxes and text boxes.

        Args:
            checked (bool): Button press status.
        """
        if checked:
            if self.ai_current_channel != self.AI_channel_combo.currentIndex():
                self.ai_task.close()
                self.ai_task = NIDAQ_ai_task('Dev1',self.AI_channel_combo.currentText())
                self.ai_current_channel = self.AI_channel_combo.currentIndex()
            
            if self.ao_current_channel != self.AO_channel_combo.currentIndex():
                self.ao_task.close()
                self.ao_task = NIDAQ_ao_task('Dev1',self.AO_channel_combo.currentText())
                self.ao_current_channel = self.AO_channel_combo.currentIndex()
                
            if self.do_current_port != self.DO_port_combo.currentIndex() or self.do_current_channel != self.DO_channel_combo.currentIndex():
                self.do_task.close()
                self.do_task = NIDAQ_do_task('Dev1',self.DO_port_combo.currentText(),self.DO_channel_combo.currentText())
                self.do_current_port = self.DO_port_combo.currentIndex()
                self.do_current_channel = self.DO_channel_combo.currentIndex()
                
            self.ai_task.start()
            self.ao_task.start()
            self.do_task.start()
            self.do_task.setDOData(False)
            
            self.threshold.setEnabled(False)
            self.vamp.setEnabled(False)
            self.step.setEnabled(False)
            self.dt.setEnabled(False)
            self.AI_channel_combo.setEnabled(False)
            self.AO_channel_combo.setEnabled(False)
            self.DO_port_combo.setEnabled(False)
            self.DO_channel_combo.setEnabled(False)
            self.lock_button.setEnabled(True)
            self.scan_button.setText('STOP')
            self.data_connector.resume()
            self.plot_running = True
        else:
            self.ai_task.stop()
            self.ao_task.stop()
            self.do_task.stop()
            
            self.threshold.setEnabled(True)
            self.vamp.setEnabled(True)
            self.step.setEnabled(True)
            self.dt.setEnabled(True)
            self.AI_channel_combo.setEnabled(True)
            self.AO_channel_combo.setEnabled(True)
            self.DO_port_combo.setEnabled(True)
            self.DO_channel_combo.setEnabled(True)
            self.lock_button.setEnabled(False)
            self.lock_button.setText('LOCK')
            self.lock_button.setChecked(False)
            self.scan_button.setText('SCAN')
            self.data_connector.pause()
            self.plot_running = False
            
    
    def slotLockButtonToggled(self, checked: bool) -> None:
        """
        A function that defines the behavior of a lock button.
        When the button is pressed, the plotting stops.
        When the button is released, the plotting begins.

        Args:
            checked (bool): Button press status.
        """
        if checked:
            self.ai_task.stop()
            self.ao_task.stop()
            self.do_task.stop()
            self.lock_button.setText('UNLOCK')
        else:
            self.ai_task.start()
            self.ao_task.start()
            self.do_task.start()
            self.lock_button.setText('LOCK')
            
    
    def plotGenerator(self, *data_connectors: tuple) -> None:
        """
        A function with a defined plotting behavior.
        Plot the current analog input values.
        
        Args:
            data_connectors (tuple): Arguments for manipulating the plot area.
        """
        x = 0
        vo = 0
        while True:
            threshold = float(self.threshold.text()) if self.threshold.text() != '' and self.threshold.text() != '-' else 0.0
            vmax = float(self.vmax.text()) if self.vmax.text() != '' and self.vmax.text() != '-' else 0.0
            vmin = float(self.vmin.text()) if self.vmin.text() != '' and self.vmin.text() != '-' else 0.0
            vamp = float(self.vamp.text()) if self.vamp.text() != '' and self.vamp.text() != '-' else 0.0
            step = float(self.step.text()) if self.step.text() != '' and self.step.text() != '-' else 0.0
            dt = float(self.dt.text()) if self.dt.text() != '' and self.dt.text() != '-' else 0.0
            slope = 1.0
            
            if self.plot_running:
                vo += slope * step
                self.ao_task.setAOData(vo)
                vi = self.ai_task.getAIData_single()[0]
                if vi > threshold:
                    time.sleep(dt/1000)
                    self.do_task.setDODatad(True)
                    slope = 0
                    
                if slope > 0 and vo > vmax:
                    slope = -1.0
                elif slope < 0 and vo < vmin:
                    slope = 1.0
                    
                for data_connector in data_connectors:
                    data_connector.cb_append_data_point(vi,x)
                    x += 1
            self.sleep(0.1e-10)
                
        
    # def scan(self):
    #     threshold = float(self.threshold.text()) if self.threshold.text() != '' and self.threshold.text() != '-' else 0.0
    #     vmax = float(self.vmax.text()) if self.vmax.text() != '' and self.vmax.text() != '-' else 0.0
    #     vmin = float(self.vmin.text()) if self.vmin.text() != '' and self.vmin.text() != '-' else 0.0
    #     vamp = float(self.vamp.text()) if self.vamp.text() != '' and self.vamp.text() != '-' else 0.0
    #     step = float(self.step.text()) if self.step.text() != '' and self.step.text() != '-' else 0.0
    #     dt = float(self.dt.text()) if self.dt.text() != '' and self.dt.text() != '-' else 0.0
    #     slope = 1.0
    #     ao = 0

    #     vo += slope*step
    #     self.ao_task.setAOData(vo)
    #     vi = self.ai_task.getAIData_single()[0]
    #     if vi > threshold:
    #         time.sleep(dt/1000)
    #         self.do_task.setDODatad(True)
    #         slope = 0
            
    #     if slope > 0 and vo > vmax:
    #         slope = -1.0
    #     elif slope < 0 and vo < vmin:
    #         slope = 1.0

    #     return vi
