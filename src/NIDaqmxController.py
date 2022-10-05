import nidaqmx
from nidaqmx.constants import LineGrouping

class NIDAQ_task:
    def __init__(self):
        """
        Constructor.
        
        Create a task
        """
        self.dev_name = self.getDeviceNames()[0]
        self.task = nidaqmx.Task()
    
    def start(self):
        self.task.start()
    
    def stop(self):
        self.task.stop()
    
    def close(self):
        self.task.close()
        
    def getDeviceNames(self) -> list:
        sys = nidaqmx.system.System()
        return sys.devices.device_names


class NIDAQ_ai_task(NIDAQ_task):
    def __init__(self, port : str):
        """
        Constructor.
        
        Create an AI task
        """
        super().__init__()
        self.task.ai_channels.add_ai_voltage_chan(self.dev_name + "/" + port)
    
    def getAIData_single(self) -> list:
        """
        Obtain an analog input value.

        Returns:
            list: Analog input values.
        """
        try:
            return self.task.read(number_of_samples_per_channel=1)
        except nidaqmx.errors.DaqReadError:
            print('error')
        
    def getAIData_multi(self, num) -> list:
        """
        Obtain an analog input value.

        Returns:
            list: Analog input values.
        """
        try:
            return self.task.read(number_of_samples_per_channel=num)
        except nidaqmx.errors.DaqReadError:
            return [False]
        

class NIDAQ_ao_task(NIDAQ_task):
    def __init__(self, port : str):
        """
        Constructor.
        
        Create an AO task
        """
        super().__init__()
        self.task.ao_channels.add_ao_voltage_chan(self.dev_name + "/" + port)
        
    def setAOData(self, data : float) -> None:
        """
        Set an analog output value.

        """
        try:
            return self.task.write(data, auto_start=False)
        except nidaqmx.errors.DaqWriteError:
            return False


class NIDAQ_do_task(NIDAQ_task):
    def __init__(self, port : str, line : str):
        """
        Constructor.
        
        Create a DO task
        """
        super().__init__()
        self.task.do_channels.add_do_chan(self.dev_name + "/" + port + "/" + line, line_grouping=LineGrouping.CHAN_PER_LINE)
    
    def setDOData(self, data : bool) -> None:
        """
        Set a digital output value.

        """
        try:
            return self.task.write(data, auto_start=False)
        except nidaqmx.errors.DaqWriteError:
            return False