from PyQt5.QtWidgets import QWidget,QTabWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QLineEdit,QComboBox,QCheckBox,QLabel
from PyQt5 import QtCore,QtGui
import pyqtgraph as pg
from pglive.kwargs import Crosshair
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget
from pglive.sources.data_connector import DataConnector
import Model
import Controller

class View(QWidget):
    def __init__(self, model: Model):
        super(QWidget, self).__init__()
        self.__model = model
        
    def register(self, controller: Controller) -> None:
        self.__controller = controller
        self.__initUI()
        
    def __initUI(self) -> None:
        layout = QVBoxLayout()
        tabs = QTabWidget()
        ai_tab = QWidget()
        ao_tab = QWidget()
        do_tab = QWidget()
        
        ai_tab.setLayout(self.__getAITabUI())
        ao_tab.setLayout(self.__getAOTabUI())
        do_tab.setLayout(self.__getDOTabUI())
        
        tabs.resize(300,200)
        
        tabs.addTab(ai_tab,'AI')
        tabs.addTab(ao_tab,'AO')
        tabs.addTab(do_tab,'DO')
        
        layout.addWidget(tabs)
        
        self.setLayout(layout)
    
    def __getAITabUI(self) -> QVBoxLayout:
        ui_information = QVBoxLayout()
        user_control_area = QHBoxLayout()
        user_control_area.addStretch(1)
        
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        self.__plot_ai = LiveLinePlot()
        plot_ai_widget = LivePlotWidget(title='Analog Input', **kwargs)
        plot_ai_widget.addItem(self.__plot_ai)
        
        ai_channels = ['ai0','ai1','ai2','ai3','ai4','ai5','ai6','ai7']
        self.__ai_channel_combo = QComboBox()
        self.__ai_channel_combo.setFixedWidth(100)
        self.__ai_channel_combo.addItems(ai_channels)
        
        self.__ai_execute_button = QPushButton('EXECUTE')
        self.__ai_execute_button.setFixedWidth(100)
        self.__ai_execute_button.setCheckable(True)
        self.__ai_execute_button.toggled.connect(self.__controller.slotAIExecuteButtonToggled)
        
        user_control_area.addWidget(self.__ai_channel_combo)
        user_control_area.addWidget(self.__ai_execute_button)
        
        ui_information.addWidget(plot_ai_widget)
        ui_information.addLayout(user_control_area)
        
        return ui_information
    
    def __getAOTabUI(self) -> QVBoxLayout:
        ui_information = QVBoxLayout()
        user_control_area = QHBoxLayout()
        user_control_area.addStretch(1)
        
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        self.__plot_ao = LiveLinePlot()
        plot_ao_widget = LivePlotWidget(title='Analog Output', **kwargs)
        plot_ao_widget.addItem(self.__plot_ao)
        
        self.__ao_textbox = QLineEdit()
        lim = QtCore.QRegExp("[0-9-.]+")
        self.__ao_textbox.setValidator(QtGui.QRegExpValidator(lim))
        self.__ao_textbox.setFixedWidth(100)
        self.__ao_textbox.setText('0.0')
        
        ao_channels = ['ao0','ao1']
        self.__ao_channel_combo = QComboBox()
        self.__ao_channel_combo.setFixedWidth(100)
        self.__ao_channel_combo.addItems(ao_channels)
        
        self.__ao_execute_button = QPushButton('EXECUTE')
        self.__ao_execute_button.setFixedWidth(100)
        self.__ao_execute_button.setCheckable(True)
        self.__ao_execute_button.toggled.connect(self.__controller.slotAOExecuteButtonToggled)
        
        user_control_area.addWidget(self.__ao_channel_combo)
        user_control_area.addWidget(self.__ao_textbox)
        user_control_area.addWidget(self.__ao_execute_button)
        
        ui_information.addWidget(plot_ao_widget)
        ui_information.addLayout(user_control_area)
        
        return ui_information
    
    def __getDOTabUI(self) -> QVBoxLayout:
        ui_information = QVBoxLayout()
        user_control_area = QHBoxLayout()
        user_control_area.addStretch(1)
        
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        self.__plot_do = LiveLinePlot()
        plot_do_widget = LivePlotWidget(title='Digital Output', **kwargs)
        plot_do_widget.addItem(self.__plot_do)
        
        do_ports = ['port0','port1','port2']
        self.__do_port_combo = QComboBox()
        self.__do_port_combo.setFixedWidth(100)
        self.__do_port_combo.addItems(do_ports)
        self.__do_port_combo.setCurrentIndex(1)
        
        do_lines = ['line0','line1','line2','line3','line4','line5','line6','line7']
        self.__do_line_combo = QComboBox()
        self.__do_line_combo.setFixedWidth(100)
        self.__do_line_combo.addItems(do_lines)
        
        self.__do_control_button = QPushButton('Set True')
        self.__do_control_button.setFixedWidth(100)
        self.__do_control_button.setCheckable(True)
        self.__do_control_button.toggled.connect(self.__controller.slotDOControlButtonToggled)
        
        self.__do_execute_button = QPushButton('EXECUTE')
        self.__do_execute_button.setFixedWidth(100)
        self.__do_execute_button.setCheckable(True)
        self.__do_execute_button.toggled.connect(self.__controller.slotDOExecuteButtonToggled)
            
        user_control_area.addWidget(self.__do_port_combo)
        user_control_area.addWidget(self.__do_line_combo)
        user_control_area.addWidget(self.__do_control_button)
        user_control_area.addWidget(self.__do_execute_button)
        
        ui_information.addWidget(plot_do_widget)
        ui_information.addLayout(user_control_area)
        
        return ui_information
    
    def getAIChannel(self) -> str:
        return self.__ai_channel_combo.currentText()
    
    def getAIChannelComboCurrentIndex(self) -> int:
        return self.__ai_channel_combo.currentIndex()
    
    def getPlotAI(self) -> LiveLinePlot:
        return self.__plot_ai
    
    def setAIChannelComboEnabled(self, state: bool) -> None:
        self.__ai_channel_combo.setEnabled(state)
        
    def setAIExecuteButtonText(self, text: str) -> None:
        self.__ai_execute_button.setText(text)
        
    def setAIExecuteButtonState(self, state: bool) -> None:
        self.__ai_execute_button.setChecked(state)
        
        
    
    def getAOChannel(self) -> str:
        return self.__ao_channel_combo.currentText()
    
    def getAOChannelComboCurrentIndex(self) -> int:
        return self.__ao_channel_combo.currentIndex()
    
    def getAOValue(self) -> float:
        return float(self.__ao_textbox.text())
    
    def getAOTextbox(self) -> str:
        return self.__ao_textbox.text()
    
    def getPlotAO(self) -> LiveLinePlot:
        return self.__plot_ao
    
    def setAOChannelComboEnabled(self, state: bool) -> None:
        self.__ao_channel_combo.setEnabled(state)
    
    def setAOTextboxEnabled(self, state: bool) -> None:
        self.__ao_textbox.setEnabled(state)
    
    def setAOExecuteButtonText(self, text: str) -> None:
        self.__ao_execute_button.setText(text)
        
    def setAOExecuteButtonState(self, state: bool) -> None:
        self.__ao_execute_button.setChecked(state)
    
    
    
    
    def getDOPort(self) -> str:
        return self.__do_port_combo.currentText()
    
    def getDOPortComboCurrentIndex(self) -> int:
        return self.__do_port_combo.currentIndex()
    
    def getDOLine(self) -> str:
        return self.__do_line_combo.currentText()
    
    def getDOLineComboCurrentIndex(self) -> int:
        return self.__do_line_combo.currentIndex()
    
    def getPlotDO(self) -> LiveLinePlot:
        return self.__plot_do
    
    def setDOPortComboEnabled(self, state: bool) -> None:
        self.__do_port_combo.setEnabled(state)
        
    def setDOLineComboEnabled(self, state: bool) -> None:
        self.__do_line_combo.setEnabled(state)
    
    def setDOControlButtonText(self, text: str) -> None:
        self.__do_control_button.setText(text)
    
    def setDOControlButtonState(self, state: bool) -> None:
        self.__do_control_button.setChecked(state)
    
    def setDOExecuteButtonText(self, text: str) -> None:
        self.__do_execute_button.setText(text)
        
    def setDOExecuteButtonState(self, state: bool) -> None:
        self.__do_execute_button.setChecked(state)
    