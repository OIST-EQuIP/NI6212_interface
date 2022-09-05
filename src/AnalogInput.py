from PyQt5.QtWidgets import QLabel

from TabCategory import TabCategory
from NIDaqmxController import NIDaqmxController

class AnalogInput(TabCategory):
    """AnalogInput Class.

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
        # Combo
        items = ['AI 0','AI 1','AI 2','AI 3','AI 4','AI 5','AI 6','AI 7']
        self.channel_combo = super().createCombo(items)
        # Button
        self.AI_button = self.createButton('EXECUTE',True)
        self.AI_button.toggled.connect(self.slotButtonToggled)
        
        # Box layout
        ## HBox
        self.hbox_main.addWidget(self.channel_combo)
        self.hbox_main.addWidget(self.AI_button)
        ## VBox
        self.vbox_main.addWidget(self.plot_widget)
        self.vbox_main.addLayout(self.hbox_main)
        
        self.tab.addLayout(self.vbox_main)
        
    
    def slotButtonToggled(self, checked: bool) -> None:
        """slotButtonToggled.

        Parameters
        ----------
        checked : bool
        
        """
        if checked:
            self.data_connector.resume()
            self.plot_running = True
            self.channel_combo.setEnabled(False)
            self.AI_button.setText('STOP')
        else:
            self.data_connector.pause()
            self.plot_running = False
            self.channel_combo.setEnabled(True)
            self.AI_button.setText('EXECUTE')
            
            
    def plotGenerator(self, *data_connectors: tuple) -> None:
        """plotGenerator.

        Parameters
        ----------
        data_connectors : tuple
        
        """
        x = 0
        while True:
            for data_connector in data_connectors:
                if self.plot_running == True:
                    channel = 'ai' + self.channel_combo.currentText()[-1]
                    value = self.ni.getAIData(channel)
                    data_connector.cb_append_data_point(value[0],x)
                    x += 1
                
            self.sleep(0.02)