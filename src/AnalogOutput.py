from PyQt5.QtWidgets import QLabel

from TabCategory import TabCategory
from NIDAQmxController import NIDAQmxController

class AnalogOutput(TabCategory):
    """
    Class that holds information on analog output tabs.

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
        # TextBox
        self.textbox = self.createTextBox("[0-9-.]+")
        self.textbox.setText('0.0')
        # Label
        self.message = self.createLabel('')
        # Combo box
        items = ['AO 0','AO 1']
        self.channel_combo = self.createCombo(items)
        # Button
        self.button = self.createButton('EXECUTE',True)
        self.button.toggled.connect(self.slotButtonToggled)
        # Box layout
        ## HBox
        self.hbox_main.addWidget(self.message)
        self.hbox_main.addWidget(self.textbox)
        self.hbox_main.addWidget(self.createLabel("V"))
        self.hbox_main.addWidget(self.channel_combo)
        self.hbox_main.addWidget(self.button)
        ## VBox
        self.vbox_main.addWidget(self.plot_widget)
        self.vbox_main.addLayout(self.hbox_main)
        
        self.tab.addLayout(self.vbox_main)
        
        
    def slotButtonToggled(self, checked: bool) -> None:
        """
        A function that defines the behavior of a button.
        When the button is pressed, the text box and combo are disabled and the plotting begins.
        When the button is released, it stops the plot and activates the text box and combo.

        Args:
            checked (bool): Button press status.
        """
        if checked:
            self.textbox.setEnabled(False)
            self.channel_combo.setEnabled(False)
            self.button.setText('STOP')
            self.data_connector.resume()
            self.plot_running = True
        else:
            self.textbox.setEnabled(True)
            self.channel_combo.setEnabled(True)
            self.button.setText('EXECUTE')
            self.data_connector.pause()
            self.plot_running = False
    
    
    def plotGenerator(self, *data_connectors: tuple) -> None:
        """
        A function with a defined plotting behavior.
        The value specified by the analog output is plotted.
        
        Args:
            data_connectors (tuple): Arguments for manipulating the plot area.
        """
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
                if self.plot_running == True: 
                    channel = 'ao' + self.channel_combo.currentText()[-1]
                    self.ni.setAOData(channel,value)
                    data_connector.cb_append_data_point(value,x)
                    x += 1
                
            self.sleep(0.02)