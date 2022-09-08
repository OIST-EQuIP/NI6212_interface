import nidaqmx
from nidaqmx.constants import (LineGrouping)

class NIDAQmxController:
    """
    Class for operating NI-DAQmx USB-6212(BUS).
    """
    def __init__(self):
        """
        Constructor.
        """
        self.dev = None


    def setDevName(self,dev_name: str) -> None:
        """
        Specify device name.

        Args:
            dev_name (str): Device name.
        """
        self.dev = dev_name
    
    
    def getDevName(self) -> str:
        """
        Get device name.

        Returns:
            str: Device name.
        """
        return self.dev
    
    
    def getAIData(self,port: str) -> list:
        """
        Obtain analog input values.

        Args:
            port (str): Port Information.

        Returns:
            list: Analog input values.
        """
        try:
            with nidaqmx.Task() as task:
                task.ai_channels.add_ai_voltage_chan(self.dev + "/" + port)
                return task.read(number_of_samples_per_channel=1)
        except nidaqmx.errors.DaqError:
            return [0]

        
    def setAOData(self,port: str,data: float) -> None:
        """
        Specify analog output value.

        Args:
            port (str): Port Information.
            data (float): Analog output value.
        """
        try:
            with nidaqmx.Task() as task:
                task.ao_channels.add_ao_voltage_chan(self.dev + "/" + port)
                task.write([data], auto_start=True)    
        except nidaqmx.errors.DaqError:
            pass
        
    
    def getDOData(self,port: str,lineCh: list) -> bool:
        """
        Obtain digital input values.

        Args:
            port (str): Port Information.
            lineCh (list): Channel Information.

        Returns:
            bool: Digital input values.
        """
        try:
            with nidaqmx.Task() as task:
                for i in lineCh:
                    task.di_channels.add_di_chan(self.dev + "/" + port + "/" + i, line_grouping=LineGrouping.CHAN_PER_LINE)
                return task.read()
        except nidaqmx.errors.DaqError:
            return False
    
    
    def setDOData(self,port: str,lineCh: list,data: bool) -> None:
        """
        Specify digital output value.

        Args:
            port (str): Port Information.
            lineCh (list): Channel Information.
            data (bool): Digital output value.
        """
        try:
            with nidaqmx.Task() as task:
                for i in lineCh:
                    task.do_channels.add_do_chan(self.dev + "/" + port + "/" + i, line_grouping=LineGrouping.CHAN_PER_LINE)
                task.write([data] * len(lineCh))
        except nidaqmx.errors.DaqError:
            pass

    
    def init(self) -> None:
        """
        Reset all ports and channels.
        """
        ao_channel = ['ao0','ao1']
        do_port = ['port0','port1','port2']
        do_channel = ['line0','line1','line2','line3','line4','line5','line6','line7']
        
        for i in ao_channel:
            self.setAOData(i,0.0)
        for i in do_port:
            self.setDOData(i,do_channel,False)