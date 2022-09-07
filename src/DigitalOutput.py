from PyQt5.QtWidgets import QLabel

from TabCategory import TabCategory
from NIDAQmxController import NIDAQmxController

class DigitalOutput(TabCategory):
    """
    Class that holds information on digital output tabs.

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
        self.DO_state = False
        # Combo box
        items = ['Port 0','Port 1','Port 2']
        self.port_combo = self.createCombo(items)
        self.port_combo.setCurrentIndex(1)
        # Checkbox
        self.checkboxes,checkboxes_layout = self.createCheckboxLayout(8)
        # Button
        self.state_button = self.createButton('ON',True)
        self.state_button.toggled.connect(self.slotStateButtonToggled)
        self.execute_button = self.createButton('EXECUTE',True)
        self.execute_button.toggled.connect(self.slotExecuteButtonToggled)
        
        # Box layout
        ## HBox
        self.hbox_main.addWidget(self.port_combo)
        self.hbox_main.addLayout(checkboxes_layout)
        self.hbox_main.addWidget(self.state_button)
        self.hbox_main.addWidget(self.execute_button)
        ## VBox
        self.vbox_main.addWidget(self.plot_widget)
        self.vbox_main.addLayout(self.hbox_main)
        
        self.tab.addLayout(self.vbox_main)
        
        
    def slotStateButtonToggled(self, checked: bool) -> None:
        """
        A function that defines the behavior of a state button.
        When the button is pressed, the digital signal status is set to True.
        When the button is released, the digital signal status is set to False.

        Args:
            checked (bool): Button press status.
        """
        if checked:
            self.state_button.setText('OFF')
            self.DO_state = True
        else:
            self.state_button.setText('ON')
            self.DO_state = False
            
    
    def slotExecuteButtonToggled(self, checked: bool) -> None:
        """
        A function that defines the behavior of a execute button.
        When the button is pressed, the combo box and checkboxes is disabled and the plotting begins.
        When the button is released, it stops the plot and activates the combo box and checkboxes.

        Args:
            checked (bool): Button press status.
        """
        if checked:
            self.port_combo.setEnabled(False)
            for i in range(len(self.checkboxes)):
                self.checkboxes[i].setEnabled(False)
            self.execute_button.setText('STOP')
            self.data_connector.resume()
            self.plot_running = True
        else:
            self.port_combo.setEnabled(True)
            for i in range(len(self.checkboxes)):
                self.checkboxes[i].setEnabled(True)
            self.execute_button.setText('EXECUTE')
            self.data_connector.pause()
            self.plot_running = False
                    

    def plotGenerator(self,*data_connectors: tuple) -> None:
        """
        A function with a defined plotting behavior.
        Plot the digital output signal.
        
        Args:
            data_connectors (tuple): Arguments for manipulating the plot area.
        """
        x = 0
        while True: 
            for data_connector in data_connectors:
                if self.plot_running == True: 
                    port = 'port' + self.port_combo.currentText()[-1]
                    select = list()
                    status = self.DO_state
                    channels = list()
                    for i in range(len(self.checkboxes)):
                        if self.checkboxes[i].checkState() == self.checked:
                            select.append(i)

                    for i in select:
                        channels.append(f'line{i}')
                    self.ni.setDOData(port,channels,status)
                    data_connector.cb_append_data_point(self.DO_state,x)
                    x += 1
                    
            self.sleep(0.02)
            
        