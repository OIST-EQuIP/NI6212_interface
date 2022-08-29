import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication
from TableWidget import TableWidget

class App(QMainWindow):
    """App class."""
    def __init__(self):
        """Constructor"""
        super().__init__()
        title = "NI6212 Interface"
        width = 855
        height = 500
        self.setWindowTitle(title)
        self.setFixedSize(width,height)
        table_widget = TableWidget(self)
        self.setCentralWidget(table_widget)
        self.show()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    os._exit(app.exec_())