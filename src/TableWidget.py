from PyQt5.QtWidgets import QPushButton, QWidget, QTabWidget, QVBoxLayout, QLineEdit, QComboBox, QLabel, QHBoxLayout
from threading import Thread

from NIDaqmx import NIDaqmx

from AnalogInput import AnalogInput
from AnalogOutput import AnalogOutput
from DigitalOutput import DigitalOutput
from ScanAmplitude import ScanAmplitude

class TableWidget(QWidget):
    def __init__(self,parent) -> None:
        super(QWidget,self).__init__(parent)
        self.ni = NIDaqmx()
        self.layout = QVBoxLayout(self)
        
        self.ch_status_value = QLabel("Crosshair: Outside plot")
        self.ch_x_value = QLabel("X: Unavailable")
        self.ch_y_value = QLabel("Y: Unavailable")
        
        self.analogInput = AnalogInput('Analog Input',self.ch_status_value,self.ch_x_value,self.ch_y_value)
        self.analogOutput = AnalogOutput('Analog Output',self.ch_status_value,self.ch_x_value,self.ch_y_value)
        self.digitalOutput = DigitalOutput('Digital Output',self.ch_status_value,self.ch_x_value,self.ch_y_value)
        self.scanAmplitude = ScanAmplitude('Scan Amplitude',self.ch_status_value,self.ch_x_value,self.ch_y_value)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,'AI')
        self.tabs.addTab(self.tab2,'AO')
        self.tabs.addTab(self.tab3,'DO')
        self.tabs.addTab(self.tab4,'Scan Amplitude')
        
        self.tab1.setLayout(self.analogInput.getLayout())
        self.tab2.setLayout(self.analogOutput.getLayout())
        self.tab3.setLayout(self.digitalOutput.getLayout())
        self.tab4.setLayout(self.scanAmplitude.getLayout())
        
        label = QLabel("Device Name")
        label.setFixedWidth(80)
        self.dev_name = QLineEdit(self)
        self.dev_name.setFixedWidth(150)
        self.dev_name.setText("Dev1")
        self.dev_name.setEnabled(False)
        self.ni.setDevName(self.dev_name.text())
        
        self.editButton = self.createButton('Edit',True)
        self.editButton.setFixedWidth(100)
        self.editButton.toggled.connect(self.slotEditButtonToggled)
        
        
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(label)
        self.hbox.addWidget(self.dev_name)
        self.hbox.addWidget(self.editButton)
        self.hbox.addWidget(self.ch_status_value)
        self.hbox.addWidget(self.ch_x_value)
        self.hbox.addWidget(self.ch_y_value)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.layout.addLayout(self.hbox)
        
        Thread(target=self.analogInput.plotGenerator, args=(self.analogInput.data_connector,)).start()
        Thread(target=self.analogOutput.plotGenerator, args=(self.analogOutput.data_connector,)).start()
        Thread(target=self.digitalOutput.plotGenerator, args=(self.digitalOutput.data_connector,)).start()
        Thread(target=self.scanAmplitude.plotGenerator, args=(self.scanAmplitude.data_connector,)).start()
    

    def createCombo(self,items: list) -> QComboBox:
        combo = QComboBox(self)
        for item in items:
            combo.addItem(item)
            
        return combo
    
    
    def createButton(self,label: str,toggled: bool) -> QPushButton:
        button = QPushButton(label)
        button.setCheckable(toggled)
        return button
    
    
    def slotEditButtonToggled(self,checked: bool) -> None:
        if checked:
            self.editButton.setText("Set")
            self.dev_name.setEnabled(True)
        else:
            self.editButton.setText("Edit")
            self.ni.setDevName(self.dev_name.text())
            self.dev_name.setEnabled(False)