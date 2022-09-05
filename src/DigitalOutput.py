from PyQt5.QtWidgets import QLabel

from TabCategory import TabCategory
from NIDaqmxController import NIDaqmxController

class DigitalOutput(TabCategory):
    """DigitalOutput Class.

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
        self.DO_state = False
        # Combo
        items = ['Port 0','Port 1','Port 2']
        self.port_combo = self.createCombo(items)
        self.port_combo.setCurrentIndex(1)
        # Checkbox
        self.checkboxs,checkboxs_layout = self.createCheckboxLayout(8)
        # Button
        self.state_button = self.createButton('ON',True)
        self.state_button.toggled.connect(self.slotStateButtonToggled)
        self.execute_button = self.createButton('EXECUTE',True)
        self.execute_button.toggled.connect(self.slotExecuteButtonToggled)
        
        # Box layout
        ## HBox
        self.hbox_main.addWidget(self.port_combo)
        self.hbox_main.addLayout(checkboxs_layout)
        self.hbox_main.addWidget(self.state_button)
        self.hbox_main.addWidget(self.execute_button)
        ## VBox
        self.vbox_main.addWidget(self.plot_widget)
        self.vbox_main.addLayout(self.hbox_main)
        
        self.tab.addLayout(self.vbox_main)
        
        
    def slotStateButtonToggled(self, checked: bool) -> None:
        """slotButtonToggled.

        Parameters
        ----------
        checked : bool
        
        """
        if checked:
            self.DO_state = True
            self.state_button.setText('OFF')
        else:
            self.DO_state = False
            self.state_button.setText('ON')
            
    
    def slotExecuteButtonToggled(self, checked: bool) -> None:
        """slotExecuteButtonToggled.

        Parameters
        ----------
        checked : bool
        
        """
        if checked:
            self.data_connector.resume()
            self.plot_running = True
            self.execute_button.setText('STOP')
        else:
            self.data_connector.pause()
            self.plot_running = False
            self.execute_button.setText('EXECUTE')
                    

    def plotGenerator(self,*data_connectors: tuple) -> None:
        """plotGenerator.

        Parameters
        ----------
        data_connectors : tuple
        
        """
        x = 0
        while True: 
            for data_connector in data_connectors:
                if self.plot_running == True: 
                    port = 'port' + self.port_combo.currentText()[-1]
                    select = list()
                    status = self.DO_state
                    channels = list()
                    for i in range(len(self.checkboxs)):
                        if self.checkboxs[i].checkState() == self.checked:
                            select.append(i)

                    for i in select:
                        channels.append(f'line{i}')
                    self.ni.setDOData(port,channels,status)
                    data_connector.cb_append_data_point(self.DO_state,x)
                    x += 1
                    
            self.sleep(0.02)
            
        