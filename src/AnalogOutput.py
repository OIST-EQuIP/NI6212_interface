from PyQt5.QtWidgets import QLabel

from TabCategory import TabCategory
from NIDAQmxController import NIDAQ_ao_task

import concurrent.futures

import queue

class AnalogOutput(TabCategory):
    """
    Class that holds information on analog output tabs.

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
        # TextBox
        self.textbox = self.createTextBox("[0-9-.]+")
        self.textbox.setText('0.0')
        # Label
        self.message = self.createLabel('')
        # Combo box
        ao_chan = ['ao0','ao1']
        self.channel_combo = self.createCombo(ao_chan)
        self.current_channel = self.channel_combo.currentIndex()
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
        
        self.ao_task = NIDAQ_ao_task(self.channel_combo.currentText())
        
        self.msg_box = queue.Queue(maxsize=100)
        
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        executor.submit(self.calc)
        executor.submit(self.plotGenerator,self.data_connector)
        
        
    def slotButtonToggled(self, checked: bool) -> None:
        """
        A function that defines the behavior of a button.
        When the button is pressed, the text box and combo are disabled and the plotting begins.
        When the button is released, it stops the plot and activates the text box and combo.

        Args:
            checked (bool): Button press status.
        """
        if checked:
            if self.current_channel != self.channel_combo.currentIndex():
                self.ao_task.close()
                self.ao_task = NIDAQ_ao_task(self.channel_combo.currentText())
                self.current_channel = self.channel_combo.currentIndex()
            self.ao_task.start()
            
            self.textbox.setEnabled(False)
            self.channel_combo.setEnabled(False)
            self.button.setText('STOP')
            self.data_connector.resume()
            self.plot_running = True
        else:
            self.ao_task.stop()
            while not self.msg_box.empty():
                self.msg_box.get()
            
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
            if self.plot_running:
                for data_connector in data_connectors:
                    data_connector.cb_append_data_point(self.msg_box.get(),x)
                    x += 1
            
            self.sleep(0.1e-3)
            
        
    def calc(self):
        while True:
            if self.plot_running:
                vo = float(self.textbox.text()) if self.textbox.text()[-1] != '' and self.textbox.text()[-1] != '-' and self.textbox.text()[0] != '.' else 0.0
                self.ao_task.setAOData(vo)
                self.msg_box.put(vo)
            
            self.sleep(0.1e-20)