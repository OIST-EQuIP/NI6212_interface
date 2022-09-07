from PyQt5.QtWidgets import QLabel

from TabCategory import TabCategory
from NIDAQmxController import NIDAQmxController

class AnalogInput(TabCategory):
    """
    Class that holds information on analog input tabs.

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
        # Combo box
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
        """
        A function that defines the behavior of a button.
        When the button is pressed, the combo box is disabled and the plotting begins.
        When the button is released, it stops the plot and activates the combo box.

        Args:
            checked (bool): Button press status.
        """
        if checked:
            self.channel_combo.setEnabled(False)
            self.AI_button.setText('STOP')
            self.data_connector.resume()
            self.plot_running = True
        else:
            self.channel_combo.setEnabled(True)
            self.AI_button.setText('EXECUTE')
            self.data_connector.pause()
            self.plot_running = False
            
            
    def plotGenerator(self, *data_connectors: tuple) -> None:
        """
        A function with a defined plotting behavior.
        Plot the value obtained from the analog input.
        
        Args:
            data_connectors (tuple): Arguments for manipulating the plot area.
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