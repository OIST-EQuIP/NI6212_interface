from PyQt5.QtWidgets import QLabel,QHBoxLayout

from TabCategory import TabCategory
from NIDaqmxController import NIDaqmxController

import math

class ScanAmplitude(TabCategory):
    """ScanAmplitude Class.

        Parameters
        ----------
        TabCategory : 
        
    """
    def __init__(self, name: str, ni: NIDaqmxController, state: QLabel, x: QLabel, y: QLabel) -> None:
        """Constructor.

        Parameters
        ----------
        name : str
            
        ni : NIDaqmx
        
        state : QLabel
        
        x : QLabel
        
        y : QLabel
        
        """
        super().__init__(name,ni,state,x,y)
        self.x = 0
        self.AO_value = 0
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
        # Combo
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
        """slotScanButtonToggled.

        Parameters
        ----------
        checked : bool
        
        """
        if checked:
            self.data_connector.resume()
            self.plot_running = True
            self.update_rate_state = True
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
            self.sleep(0.02)
        else:
            self.data_connector.pause()
            self.plot_running = False
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
            
    
    def slotLockButtonToggled(self, checked: bool) -> None:
        """slotLockButtonToggled.

        Parameters
        ----------
        checked : bool
        
        """
        if checked:
            self.data_connector.pause()
            self.plot_running = False
            self.lock_button.setText('UNLOCK')
        else:
            self.data_connector.resume()
            self.plot_running = True
            self.lock_button.setText('LOCK')
            
    
    def plotGenerator(self, *data_connectors: tuple) -> None:
        """plotGenerator.

        Parameters
        ----------
        data_connectors : tuple
        
        """
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
                    
                    AI_value = self.ni.getAIData(AI_channel)[0]
                    
                    data_connector.cb_append_data_point(AI_value,self.x)
                    
                    print(math.isclose(threshold,AI_value,rel_tol=0.01))
                    if math.isclose(threshold,AI_value,rel_tol=0.01):
                        AO_value = threshold
                        self.detection(DO_port,DO_channel,dt)
                    else:
                        AO_value = self.AOUpdateRate(vmax,vmin,vamp,step,AI_value)
                    
                    self.ni.setAOData(AO_channel,AO_value)
                    
                    self.x += 1
                
            self.sleep(0.02)
    
    
    def AOUpdateRate(self, vmax: float, vmin: float, vamp: float, step: float, now: float) -> float:
        """AOUpdateRate.

        Parameters
        ----------
        vmax : float
        
        
        vmin : float
        
        
        vamp : float
        
        
        step : float
        
        
        now : float
        
        Returns
        -------
        result : float
        
        
        """
        print(f'step: {step}')
        
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
  
        print(result)
        print(f'vamp: {mVamp}')
            
        return result
    
     
    def detection(self,do_port: str, do_channel: str, dt: float) -> None:
        """detection.
        
        Parameters
        ----------
        do_port : str
            
        
        do_channel : str
        
        
        dt : float
            
            
        """
        if not self.detection_state:
            self.sleep(dt/1000)
            self.detection_state = True
            self.ni.setDOData(do_port,[do_channel],True)