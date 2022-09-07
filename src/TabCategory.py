from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QComboBox, QLabel, QCheckBox, QHBoxLayout
from PyQt5 import QtCore,QtGui

import pyqtgraph as pg

from pglive.kwargs import Crosshair
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

import numpy as np

from time import sleep

from NIDAQmxController import NIDAQmxController

from typing import Tuple

class TabCategory:
    """
    Class that holds tab information.
    """
    def __init__(self, name: str, ni: NIDAQmxController, state: QLabel, x: QLabel, y: QLabel):
        """
        Constructor.

        Args:
            name (str): Plot Title.
            ni (NIDAQmxController): NI-DAQmx Controller Class.
            state (QLabel): Label to indicate whether the mouse cursor is in the plot area.
            x (QLabel): Label to display x-coordinates of the plot area selected by the mouse cursor.
            y (QLabel): Label to display y-coordinates of the plot area selected by the mouse cursor.
        """
        self.tab = QVBoxLayout()
        self.hbox_main = QHBoxLayout()
        self.hbox_main.addStretch(1)
        self.vbox_main = QVBoxLayout()
        self.vbox_main.addStretch(1)
        self.plot_running = False
        self.np = np
        self.sleep = sleep
        self.checked = QtCore.Qt.Checked
        
        self.crosshair_moved_message = []
        self.crosshair_out_message = []
        self.crosshair_in_message = []
        
        self.ni = ni
        self.ch_status_value = state
        self.ch_x_value = x
        self.ch_y_value = y
        
        kwargs = {Crosshair.ENABLED: True,Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),Crosshair.TEXT_KWARGS: {"color": "green"}}
        self.plot_widget = LivePlotWidget(title=name, **kwargs)
        plot = LiveLinePlot()
        self.plot_widget.addItem(plot)
        ## Connect plot with DataConnector
        self.data_connector = DataConnector(plot, max_points=200)
        self.data_connector.pause()
        ## Connect moved and out signals with respective functions
        self.plot_widget.sig_crosshair_moved.connect(self.crosshair_moved)
        self.plot_widget.sig_crosshair_out.connect(self.crosshair_out)
        self.plot_widget.sig_crosshair_in.connect(self.crosshair_in)
    
    
    def getLayout(self) -> QVBoxLayout:
        """
        Get the tab layout.

        Returns:
            QVBoxLayout: Layout Information.
        """
        return self.tab

    
    def createCombo(self, items: list) -> QComboBox:
        """
        Create a combo box.

        Args:
            items (list): Items to be used when creating combo box.

        Returns:
            QComboBox: Combo box.
        """
        combo = QComboBox()
        for item in items:
            combo.addItem(item)
            
        return combo
    
    
    def createButton(self, label: str, toggled: bool) -> QPushButton:
        """
        Create a button.

        Args:
            label (str): String to be displayed on the button.
            toggled (bool): Variable specifying the toggled mode.

        Returns:
            QPushButton: Button.
        """
        button = QPushButton(label)
        button.setCheckable(toggled)
        return button
    
    
    def createTextBox(self, limit: str, width: int = 100) -> QLineEdit:
        """
        Create a text box

        Args:
            limit (str): Input Limit Information.
            width (int, optional): Text box width. Defaults to 100.

        Returns:
            QLineEdit: Text box.
        """
        textbox = QLineEdit()
        lim = QtCore.QRegExp(limit)
        textbox.setValidator(QtGui.QRegExpValidator(lim))
        textbox.setFixedWidth(width)
        return textbox
    
    
    def createLabel(self, value: str) -> QLabel:
        """
        Create a label.

        Args:
            value (str): String to be displayed on the label.

        Returns:
            QLabel: Label.
        """
        label = QLabel(value)
        return label
    
    
    def createCheckbox(self) -> QCheckBox:
        """
        Create a checkbox.

        Returns:
            QCheckBox: Checkbox.
        """
        checkbox = QCheckBox()
        return checkbox
    
    
    def createCheckboxLayout(self, r: int) -> Tuple[list, QHBoxLayout]:
        """
        Create as many checkboxes as specified in the argument.

        Args:
            r (int): Designated quantity.

        Returns:
            Tuple[list, QHBoxLayout]: Checkboxes Information.
                                      Returns multiple checkboxes and layout information.
        """
        checkboxs = list()
        labels = list()
        vboxs = list()
        for i in range(r):
            checkboxs.append(QCheckBox())
            labels.append(QLabel(str(i)))
            labels[i].setAlignment(QtCore.Qt.AlignCenter)
            vboxs.append(QVBoxLayout())
            vboxs[i].addWidget(checkboxs[i])
            vboxs[i].addWidget(labels[i])
            
        checkbox_layout = QHBoxLayout()
        for i in vboxs:
            checkbox_layout.addLayout(i) 
            
        return checkboxs,checkbox_layout   
            
    
    def crosshair_moved(self, crosshair_pos: QtCore.QPointF) -> None:
        """
        Display the mouse cursor position in the plot area as a numerical value.
        
        Args:
            crosshair_pos (QtCore.QPointF): Mouse cursor position.
        """
        self.ch_x_value.setText(f"X: {crosshair_pos.x()}")
        self.ch_y_value.setText(f"Y: {crosshair_pos.y()}")


    def crosshair_out(self) -> None:
        """
        Indicate that the mouse cursor is outside the plot area.
        """
        self.ch_status_value.setText("Crosshair: Outside plot")
        self.ch_x_value.setText(f"X: Unavailable")
        self.ch_y_value.setText(f"Y: Unavailable")


    def crosshair_in(self) -> None:
        """
        Indicates that the mouse cursor is in the plot area.
        """
        self.ch_status_value.setText("Crosshair: Inside plot")
        