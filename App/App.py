import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from TableWidget import TableWidget
import pglive.examples_pyqt5 as examples
import signal

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "App"
        self.width = 855
        self.height = 500
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width,self.height)
        
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    