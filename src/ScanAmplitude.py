from TabCategory import TabCategory

from PyQt5.QtWidgets import QHBoxLayout

class ScanAmplitude(TabCategory):
    def __init__(self, name,ni,state,x,y):
        super().__init__(name,ni,state,x,y)
        self.detection = False
        self.x = 0
        self.AO_value = 0
        self.state = True
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
        hbox6.addWidget(self.createLabel('TTL dt'))
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
        
    
    def slotScanButtonToggled(self,checked: bool) -> None:
        if checked:
            
            self.data_connector.resume()
            self.plot_running = True
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
        else:
            self.plotInit()
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
            
    
    def slotLockButtonToggled(self,checked: bool) -> None:
        if checked:
            self.data_connector.pause()
            self.plot_running = False
            self.lock_button.setText('UNLOCK')
        else:
            self.data_connector.resume()
            self.plot_running = True
            self.lock_button.setText('LOCK')
            
    
    def plotGenerator(self,*data_connectors: tuple) -> None:
        
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
                    
                    self.AO_value,self.state = self.AOUpdateRate(vmax,vmin,vamp,step,self.AO_value,self.state)
                    self.ni.setAOData(AO_channel,self.AO_value)
                    
                    self.AI_value = self.ni.getAIData(AI_channel)[0]
                    data_connector.cb_append_data_point(self.AI_value,self.x)
                    
                    self.ScanAmplitude(threshold,self.AI_value,DO_port,DO_channel,dt)
                    
                    self.x += 1
                
            self.sleep(0.02)
        
        
    def AOUpdateRate(self,vmax: float,vmin: float,vamp: float,step: float,now_value: float,now_state: bool) -> float:        
        if self.detection:
            result = now_value
            state = False
        elif now_state:
            result = now_value + step
            state = now_state if result < vmax and self.np.abs(result) < vamp else not(now_state)
        else:
            result = now_value - step 
            state = now_state if result > vmin and self.np.abs(result) < vamp else not(now_state)
        
        print(result)
        
        return result,state
    

    def ScanAmplitude(self,threshold: float,now: float, port: str, channel: str, dt: float) -> None:
        if threshold >= now:
            self.detection = True
            self.sleep(dt/1000)
            self.ni.setDOData(port,[channel],[True])
            
    
    def plotInit(self):
        super().plotInit()
        self.x = 0
        self.AO_value = 0
        self.state = True
        
        