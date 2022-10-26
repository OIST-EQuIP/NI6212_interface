import time
import queue
import Model
import View
from NIDAQmxController import NIDAQ_ai_task,NIDAQ_ao_task,NIDAQ_do_task
from pglive.sources.data_connector import DataConnector

class Controller(object):
    def __init__(self, model: Model, view: View):
        self.__model = model
        self.__view = view
        self.__view.register(self)
        
        self.__ai_task = NIDAQ_ai_task()
        self.__ao_task = NIDAQ_ao_task()
        self.__do_task = NIDAQ_do_task()
        
        self.__ai_plot_status = False
        self.__ao_plot_status = False
        self.__do_plot_status = False
        self.__do_status = False
        
        self.__ai_plot_counter = 0       
        self.__ao_plot_counter = 0        
        self.__do_plot_counter = 0
        
        self.__ai_msg_box = queue.Queue(maxsize=500)
        self.__ao_msg_box = queue.Queue(maxsize=500)
        self.__do_msg_box = queue.Queue(maxsize=500)
        
        self.__ai_plot_data_connector = DataConnector(self.__view.getPlotAI(), max_points=300, update_rate=100)
        self.__ai_plot_data_connector.pause()
        
        self.__ao_plot_data_connector = DataConnector(self.__view.getPlotAO(), max_points=300, update_rate=100)
        self.__ao_plot_data_connector.pause()
        
        self.__do_plot_data_connector = DataConnector(self.__view.getPlotDO(), max_points=300, update_rate=100)
        self.__do_plot_data_connector.pause()
        
        self.__initTask()
        self.__seveUserSelectInformation()
        
    def __initTask(self) -> None:
        self.__ai_task.createTask(self.__view.getAIChannel())
        self.__ai_task.start()
        self.__ao_task.createTask(self.__view.getAOChannel())
        self.__ao_task.start()
        self.__do_task.createTask(self.__view.getDOPort(),self.__view.getDOLine())
        self.__do_task.start()
    
    def __seveUserSelectInformation(self) -> None:
        self.__ai_old_channel_index = self.__view.getAIChannelComboCurrentIndex()
        self.__ao_old_channel_index = self.__view.getAOChannelComboCurrentIndex()
        self.__do_old_port_index = self.__view.getDOPortComboCurrentIndex()
        self.__do_old_line_index = self.__view.getDOLineComboCurrentIndex()
    
    def updateAIData(self):
        if self.__ai_plot_status:
            self.__ai_msg_box.put(self.__ai_task.getAIData_single()[0])
    
    def slotAIExecuteButtonToggled(self, checked: bool) -> None:
        if checked:
            if self.__ai_old_channel_index != self.__view.getAIChannelComboCurrentIndex():
                self.__ai_task.createTask(self.__view.getAIChannel())
                self.__ai_task.start()
            self.__ai_plot_status = True
            self.__ai_plot_data_connector.resume()
            self.__view.setAIChannelComboEnabled(False)
            self.__view.setAIExecuteButtonText('STOP')
            self.__ai_old_channel_index = self.__view.getAIChannelComboCurrentIndex()
        else:
            while not self.__ai_msg_box.empty():
                self.__ai_msg_box.get()
            self.__ai_plot_status = False
            self.__ai_plot_data_connector.pause()
            self.__view.setAIChannelComboEnabled(True)
            self.__view.setAIExecuteButtonText('EXECUTE')
            
    def aiPlotGenerator(self, *data_connectors: tuple) -> None:
        if self.__ai_plot_status:
            for data_connector in data_connectors:
                data_connector.cb_append_data_point(self.__getAIMsgBox(),self.__ai_plot_counter)
                self.__ai_plot_counter += 1
    
    def __getAIMsgBox(self) -> float:
        if self.__ai_msg_box.empty():
            return 0.0
        else:
            return self.__ai_msg_box.get()
    
    def getAIPlotDataConnector(self) -> DataConnector:
        return self.__ai_plot_data_connector
    
    def updateAOData(self):
        if self.__ao_plot_status:
            self.__ao_task.setAOData(self.__view.getAOValue())
            self.__ao_msg_box.put(self.__view.getAOValue())
    
    def slotAOExecuteButtonToggled(self, checked: bool) -> None:
        if checked:
            if self.__ao_old_channel_index != self.__view.getAOChannelComboCurrentIndex():
                self.__ao_task.createTask(self.__view.getAOChannel())
                self.__ao_task.start()
            self.__ao_plot_status = True
            self.__ao_plot_data_connector.resume()
            self.__view.setAOChannelComboEnabled(False)
            self.__view.setAOTextboxEnabled(False)
            self.__view.setAOExecuteButtonText('STOP')
            self.__ao_old_channel_index = self.__view.getAOChannelComboCurrentIndex()
        else:
            while not self.__ao_msg_box.empty():
                self.__ao_msg_box.get()
            self.__ao_plot_status = False
            self.__ao_plot_data_connector.pause()
            self.__view.setAOChannelComboEnabled(True)
            self.__view.setAOTextboxEnabled(True)
            self.__view.setAOExecuteButtonText('EXECUTE')
    
    def aoPlotGenerator(self, *data_connectors: tuple) -> None:
        if self.__ao_plot_status:
            for data_connector in data_connectors:
                data_connector.cb_append_data_point(self.__getAOMsgBox(),self.__ao_plot_counter)
                self.__ao_plot_counter += 1
    
    def __getAOMsgBox(self) -> float:
        if self.__ao_msg_box.empty():
            return 0.0
        else:
            return self.__ao_msg_box.get()
         
    def getAOPlotDataConnector(self) -> DataConnector:
        return self.__ao_plot_data_connector
    

    
    def updateDOData(self):
        if self.__do_plot_status:
            self.__do_task.setDOData(self.__do_status)
            self.__do_msg_box.put(self.__do_status)
    
    def slotDOControlButtonToggled(self, checked: bool) -> None:
        if checked:
            self.__do_status = True
            self.__view.setDOControlButtonText('Set False')
        else:
            self.__do_status = False
            self.__view.setDOControlButtonText('Set True')
    
    def slotDOExecuteButtonToggled(self, checked: bool) -> None:
        if checked:
            if self.__do_old_port_index != self.__view.getDOPortComboCurrentIndex() or self.__do_old_line_index != self.__view.getDOLineComboCurrentIndex():
                self.__do_task.createTask(self.__view.getDOPort(),self.__view.getDOLine())
                self.__do_task.start()
                
            self.__do_plot_status = True
            self.__do_plot_data_connector.resume()
            self.__view.setDOPortComboEnabled(False)
            self.__view.setDOLineComboEnabled(False)
            self.__view.setDOExecuteButtonText('STOP')
            self.__do_old_port_index = self.__view.getDOPortComboCurrentIndex()
            self.__do_old_line_index = self.__view.getDOLineComboCurrentIndex()
        else:
            while not self.__do_msg_box.empty():
                self.__do_msg_box.get()
            self.__do_plot_status = False
            self.__do_plot_data_connector.pause()
            self.__view.setDOPortComboEnabled(True)
            self.__view.setDOLineComboEnabled(True)
            self.__view.setDOExecuteButtonText('EXECUTE')
            
    def doPlotGenerator(self, *data_connectors: tuple) -> None:
        if self.__do_plot_status:
            for data_connector in data_connectors:
                data_connector.cb_append_data_point(self.__getDOMsgBox(),self.__do_plot_counter)
                self.__do_plot_counter += 1
    
    def __getDOMsgBox(self) -> float:
        if self.__do_msg_box.empty():
            return 0.0
        else:
            return self.__do_msg_box.get()
    
    def getDOPlotDataConnector(self) -> DataConnector:
        return self.__do_plot_data_connector