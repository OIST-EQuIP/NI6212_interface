from PyQt5.QtWidgets import QLabel,QHBoxLayout

from TabCategory import TabCategory
from NIDAQmxController import NIDAQmxController

import math

class ScanAmplitude(TabCategory):
    """
    Class that holds information on scan amplitude tabs.

    Args:
        TabCategory (_type_): Parent class.
    """
    def __init__(self, name: str, ni: NIDAQmxController, state: QLabel, x: QLabel, y: QLabel) -> None:
        """
        Constructor.

        Args:
            name (str): Plot Title.
            ni (NIDAQmxController): NI-DAQmx Controller Class.
            state (QLabel): Label to indicate whether the mouse cursor is in the plot area.
            x (QLabel): Label to display x-coordinates of the plot area selected by the mouse cursor.
            y (QLabel): Label to display y-coordinates of the plot area selected by the mouse cursor.
        """
        super().__init__(name,ni,state,x,y)
        self.update_rate_state = True
        self.detection_state = False
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
        items = ['AO 0','AO 1']
        self.AO_channel_combo = self.createCombo(items)
        items = ['AI 0','AI 1','AI 2','AI 3','AI 4','AI 5','AI 6','AI 7']
        self.AI_channel_combo = self.createCombo(items)
        items = ['Port 0','Port 1','Port 2']
        self.DO_port_combo = self.createCombo(items)
        self.DO_port_combo.setCurrentIndex(1)
        items = ['PFI 0','PFI 1','PFI 2','PFI 3','PFI 4','PFI 5','PFI 6','PFI 7']
        self.DO_channel_combo = self.createCombo(items)
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
        
    
    def slotScanButtonToggled(self, checked: bool) -> None:
        """
        A function that defines the behavior of a scan button.
        When the button is pressed, the combo boxes and text boxes are disabled and the plotting begins.
        When the button is released, it stops the plot and activates the combo boxes and text boxes.

        Args:
            checked (bool): Button press status.
        """
        if checked:
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
            self.update_rate_state = True
            self.sleep(0.02)
        else:
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
            self.lock_button.setText('UNLOCK')
            self.data_connector.pause()
            self.plot_running = False
        else:
            self.lock_button.setText('LOCK')
            self.data_connector.resume()
            self.plot_running = True
            
    
    def plotGenerator(self, *data_connectors: tuple) -> None:
        """
        A function with a defined plotting behavior.
        Plot the current analog input values.
        
        Args:
            data_connectors (tuple): Arguments for manipulating the plot area.
        """
        x = 0
        while True:
            for data_connector in data_connectors:
                if self.plot_running == True:
                    threshold = float(self.threshold.text()) if self.threshold.text() != '' and self.threshold.text() != '-' else 0.0
                    vmax = float(self.vmax.text()) if self.vmax.text() != '' and self.vmax.text() != '-' else 0.0
                    vmin = float(self.vmin.text()) if self.vmin.text() != '' and self.vmin.text() != '-' else 0.0
                    vamp = float(self.vamp.text()) if self.vamp.text() != '' and self.vamp.text() != '-' else 0.0
                    step = float(self.step.text()) if self.step.text() != '' and self.step.text() != '-' else 0.0
                    dt = float(self.dt.text()) if self.dt.text() != '' and self.dt.text() != '-' else 0.0
                    AI_channel = 'ai' + self.AI_channel_combo.currentText()[-1]
                    AO_channel = 'ao' + self.AO_channel_combo.currentText()[-1]
                    DO_port = 'port' + self.DO_port_combo.currentText()[-1]
                    DO_channel = 'line' + self.DO_channel_combo.currentText()[-1]
                    
                    # AI_value = round(self.ni.getAIData(AI_channel)[0],len(str(step).split('.')[1]))
                    
                    # data_connector.cb_append_data_point(AI_value,x)
                    
                    # tol = round(0.1**(len(str(step).split('.')[1])),len(str(step).split('.')[1]))
                    
                    # if math.isclose(threshold,AI_value,abs_tol=tol):
                    #     AO_value = threshold
                    #     self.detection(DO_port,DO_channel,dt)
                    # else:
                    #     AO_value = round(self.AOUpdateRate(vmax,vmin,vamp,step,AI_value),len(str(step).split('.')[1]))
                    
                    # print(f'tol: {tol}, AI: {AI_value}, AO: {AO_value}')
                    
                    AI_value = self.ni.getAIData(AI_channel)[0]
                    
                    data_connector.cb_append_data_point(AI_value,x)
                    
                    if threshold >= 0 and AI_value >= threshold or threshold < 0 and AI_value <= threshold:
                        # AO_value = threshold
                        self.detection(DO_port,DO_channel,dt)
                    elif threshold >= 0 and AI_value < threshold or threshold < 0 and AI_value > threshold:
                        AO_value = self.AOUpdateRate(vmax,vmin,vamp,step,AI_value)
                    
                    self.ni.setAOData(AO_channel,AO_value)
                    self.ni.setAOData('ao1',AO_value)
                    
                    print(f'AI: {AI_value}, AO: {AO_value}')
                    
                    x += 1
                
            self.sleep(0.02)
    
    
    def AOUpdateRate(self, vmax: float, vmin: float, vamp: float, step: float, now: float) -> float:        
        """
        This class is used to calculate analog output values.
        Increase or decrease the analog output value according to the step size.

        Args:
            vmax (float): Maximum output value.
            vmin (float): Minimum output value.
            vamp (float): Specified output value limit.
            step (float): Step size.
            now (float): Current analog output value.

        Returns:
            float: Calculated analog output value.
        """
        if vamp > vmax or vamp < vmin:
            mVamp = max(vmax,-(vmin))
        else:
            mVamp = vamp
        
        if self.update_rate_state:
            result = now + step
            if step > 0 and result >= mVamp: 
                self.update_rate_state = not self.update_rate_state
                result = mVamp
            if step < 0 and result <= -(mVamp): 
                self.update_rate_state = not self.update_rate_state
                result = -(mVamp)
        else:
            result = now - step
            if step > 0 and result <= -(mVamp):
                self.update_rate_state = not self.update_rate_state
                result = -(mVamp)
            if step < 0 and result >= mVamp:
                self.update_rate_state = not self.update_rate_state
                result = mVamp
                
        return result
    
     
    def detection(self,do_port: str, do_channel: str, dt: float) -> None:
        """
        A function that defines the action to be taken when the analog input value reaches a threshold value.
        Outputs a digital signal after ms specified by the argument dt.

        Args:
            do_port (str): Digital output port information.
            do_channel (str): Digital output channel information.
            dt (float): Designated waiting time.
        """
        if not self.detection_state:
            self.sleep(dt/1000)
            self.detection_state = True
            self.ni.setDOData(do_port,[do_channel],True)