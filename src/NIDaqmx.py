import nidaqmx
from nidaqmx.constants import (LineGrouping)

class NIDaqmx:
    def __init__(self):
        self.dev = None


    def setDevName(self,dev_name: str) -> None:
        self.dev = dev_name
    
    
    def getAIData(self,port: str) -> list:
        try:
            with nidaqmx.Task() as task:
                task.ai_channels.add_ai_voltage_chan(self.dev + "/" + port)
                return task.read(number_of_samples_per_channel=1)
        except nidaqmx.errors.DaqError:
            return [0]

        
    def setAOData(self,port: str,data: float) -> None:
        try:
            with nidaqmx.Task() as task:
                task.ao_channels.add_ao_voltage_chan(self.dev + "/" + port)
                task.write([data], auto_start=True)    
        except nidaqmx.errors.DaqError:
            pass
        
        
    def setDOData(self,port: str,lineCh: list,data: list) -> None:
        try:
            with nidaqmx.Task() as task:
                for i in lineCh:
                    task.do_channels.add_do_chan(self.dev + "/" + port + "/" + i, line_grouping=LineGrouping.CHAN_PER_LINE)
                task.write(data)
        except nidaqmx.errors.DaqError:
            pass