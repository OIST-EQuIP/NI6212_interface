from PyQt5.QtWidgets import QPushButton, QWidget, QTabWidget, QVBoxLayout, QLineEdit, QComboBox, QLabel, QHBoxLayout
from threading import Thread
import asyncio

from AnalogInput import AnalogInput
from AnalogOutput import AnalogOutput
from DigitalOutput import DigitalOutput
from ScanAmplitude import ScanAmplitude

class TableWidget(QWidget):
    """
    Widget Display Class.

    Args:
        QWidget (_type_): PyQt widget classes.
    """
    def __init__(self, parent) -> None:
        """
        Constructor.

        Args:
            parent (_type_): Parent class.
        """
        super(QWidget,self).__init__(parent)
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
        
        # label = QLabel("Device Name")
        # label.setFixedWidth(70)
        # self.dev_name = QLineEdit(self)
        # self.dev_name.setFixedWidth(100)
        # self.dev_name.setText("Dev1")
        # self.dev_name.setEnabled(False)
        
        # self.editButton = self.createButton('Edit',True)
        # self.editButton.setFixedWidth(70)
        # self.editButton.toggled.connect(self.slotEditButtonToggled)
        
        # self.init_label = QLabel('')
        # self.init_label.setFixedWidth(100)
        # self.initButton = self.createButton('Init',False)
        # self.initButton.setFixedWidth(70)
        # self.initButton.clicked.connect(self.initButtonClicked) 
        
        # self.hbox = QHBoxLayout()
        # self.hbox.addWidget(label)
        # self.hbox.addWidget(self.dev_name)
        # self.hbox.addWidget(self.editButton)
        # self.hbox.addWidget(self.ch_status_value)
        # self.hbox.addWidget(self.ch_x_value)
        # self.hbox.addWidget(self.ch_y_value)
        # self.hbox.addWidget(self.init_label)
        # self.hbox.addWidget(self.initButton)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        # self.layout.addLayout(self.hbox)
        
        # Thread(target=self.analogInput.plotGenerator, args=(self.analogInput.data_connector,)).start()
        # Thread(target=self.analogOutput.plotGenerator, args=(self.analogOutput.data_connector,)).start()
        # Thread(target=self.digitalOutput.plotGenerator, args=(self.digitalOutput.data_connector,)).start()
        # Thread(target=self.scanAmplitude.plotGenerator, args=(self.scanAmplitude.data_connector,)).start()

        
    
    # def createButton(self, label: str, toggled: bool) -> QPushButton:
    #     """
    #     Create a button.

    #     Args:
    #         label (str): String to be displayed on the button.
    #         toggled (bool): Variable specifying the toggled mode.

    #     Returns:
    #         QPushButton: Button.
    #     """
    #     button = QPushButton(label)
    #     button.setCheckable(toggled)
    #     return button
    
    
    # def slotEditButtonToggled(self, checked: bool) -> None:
    #     """
    #     A function that defines the behavior of a edit button.
    #     When the button is pressed, it activates the text box and allows the user to edit the device name.
    #     When the button is released, it saves the edited information and deactivates the text box.

    #     Args:
    #         checked (bool): Button press status.
            
    #     """
    #     if checked:
    #         self.editButton.setText("Set")
    #         self.dev_name.setEnabled(True)
    #     else:
    #         self.editButton.setText("Edit")
    #         self.ni.setDevName(self.dev_name.text())
    #         self.dev_name.setEnabled(False)
            
    
    # def initButtonClicked(self) -> None:
    #     """
    #     A function that defines the behavior of a init button.
    #     When the button is pressed, all ports are reset.
    #     """
    #     self.scanAmplitude.detection_state = False
    #     self.ni.init()
        
