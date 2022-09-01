import nidaqmx
from nidaqmx.constants import (LineGrouping)

class NIDaqmx:
    """Class to control NIDAQ devices."""
    def __init__(self):
        """Constructor.
        """
        self.dev = None


    def setDevName(self,dev_name: str) -> None:
        """Specify NIDAQ device name.

        Set to use the NIDAQ device specified in the 'dev_name' argument.

        Parameters
        ----------
        dev_name : str
            Device name to be specified
        """
        self.dev = dev_name
    
    
    def getDevName(self) -> str:
        return self.dev
    
    
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
        
        
    def setDOData(self,port: str,lineCh: list,data: bool) -> None:
        try:
            with nidaqmx.Task() as task:
                for i in lineCh:
                    task.do_channels.add_do_chan(self.dev + "/" + port + "/" + i, line_grouping=LineGrouping.CHAN_PER_LINE)
                task.write([data] * len(lineCh))
        except nidaqmx.errors.DaqError:
            pass
    
    
    def getDOData(self,port: str,lineCh: list) -> bool:
        # try:
        #     with nidaqmx.Task() as task:
        #         for i in lineCh:
        #             task.do_channels.add_do_chan(self.dev + "/" + port + "/" + i, line_grouping=LineGrouping.CHAN_PER_LINE)
        #         return task.read()
        # except nidaqmx.errors.DaqError:
        #     return False
        with nidaqmx.Task() as task:
            for i in lineCh:
                task.di_channels.add_di_chan(self.dev + "/" + port + "/" + i, line_grouping=LineGrouping.CHAN_PER_LINE)
            return task.read()