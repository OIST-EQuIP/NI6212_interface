from PyQt5.QtWidgets import QLabel

from TabCategory import TabCategory
from NIDAQmxController import NIDAQ_do_task

import concurrent.futures

import queue

class DigitalOutput(TabCategory):
    """
    Class that holds information on digital output tabs.

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
        self.DO_state = False
        # Combo box
        port = ['port0','port1','port2']
        self.port_combo = self.createCombo(port)
        self.port_combo.setCurrentIndex(1)
        self.current_port = self.port_combo.currentIndex()
        # Checkbox
        line = ['line0', 'line1', 'line2', 'line3', 'line4', 'line5', 'line6', 'line7']
        self.line_combo = self.createCombo(line)
        self.current_line = self.line_combo.currentIndex()
        # Button
        self.state_button = self.createButton('ON',True)
        self.state_button.toggled.connect(self.slotStateButtonToggled)
        self.execute_button = self.createButton('EXECUTE',True)
        self.execute_button.toggled.connect(self.slotExecuteButtonToggled)
        
        # Box layout
        ## HBox
        self.hbox_main.addWidget(self.port_combo)
        self.hbox_main.addWidget(self.line_combo)
        self.hbox_main.addWidget(self.state_button)
        self.hbox_main.addWidget(self.execute_button)
        ## VBox
        self.vbox_main.addWidget(self.plot_widget)
        self.vbox_main.addLayout(self.hbox_main)
        
        self.tab.addLayout(self.vbox_main)
        
        self.do_task = NIDAQ_do_task(self.port_combo.currentText(),self.line_combo.currentText())
        
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        executor.submit(self.calc)
        executor.submit(self.plotGenerator,self.data_connector)
        
        
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
            if self.current_port != self.port_combo.currentIndex() or self.current_line != self.line_combo.currentIndex():
                self.do_task.close()
                self.do_task = NIDAQ_do_task(self.port_combo.currentText(),self.line_combo.currentText())
                self.current_port = self.port_combo.currentIndex()
                self.current_line = self.line_combo.currentIndex()
            self.do_task.start()
            
            self.port_combo.setEnabled(False)
            self.line_combo.setEnabled(False)
            self.execute_button.setText('STOP')
            self.data_connector.resume()
            self.plot_running = True
        else:
            self.do_task.stop()
            
            self.port_combo.setEnabled(True)
            self.line_combo.setEnabled(True)
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
            if self.plot_running:
                for data_connector in data_connectors:
                    data_connector.cb_append_data_point(self.DO_state,x)
                    x += 1
            self.sleep(0.1e-3)
            
    
    def calc(self):
        while True:
            if self.plot_running:
                self.do_task.setDOData(self.DO_state)
            self.sleep(0.1e-20)
        