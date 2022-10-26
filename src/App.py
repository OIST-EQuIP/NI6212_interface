import sys
import os
from threading import Thread
from PyQt5.QtWidgets import QMainWindow, QApplication
from pglive.sources.data_connector import DataConnector
from Model import Model
from View import View
from Controller import Controller

class App(QMainWindow):
    """
    Main class.
    """
    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        
        model = Model()
        view = View(model)
        controller = Controller(model,view)
        
        title = "NI6212 Interface"
        width = 855
        height = 500
        
        Thread(target=self.main_thread, args=(controller,)).start()
        
        self.setWindowTitle(title)
        self.setFixedSize(width,height)
        self.setCentralWidget(view)
        self.show()
        
    def main_thread(self, controller: Controller) -> None:
        ai_plot_data_connector = controller.getAIPlotDataConnector()
        ao_plot_data_connector = controller.getAOPlotDataConnector()
        do_plot_data_connector = controller.getDOPlotDataConnector()
        while True:
            self.nidaq_thread(controller)
            self.plot_thread(controller, ai_plot_data_connector, ao_plot_data_connector, do_plot_data_connector)

    def nidaq_thread(self, controller: Controller):
        controller.updateAIData()
        controller.updateAOData()
        controller.updateDOData()
    
    def plot_thread(self, controller: Controller, ai_data_connector: DataConnector, ao_data_connector: DataConnector, do_data_connector: DataConnector):
        controller.aiPlotGenerator(ai_data_connector,)
        controller.aoPlotGenerator(ao_data_connector,)
        controller.doPlotGenerator(do_data_connector,)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    os._exit(app.exec_())