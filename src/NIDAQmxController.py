import nidaqmx
from nidaqmx.constants import LineGrouping

class NIDAQ_task(object):
    def __init__(self):
        """
        Constructor.
        
        Create a task
        """
        self._dev_name = self.__getDeviceNames()[0]
    
    def createTask(self) -> None:
        self._task = nidaqmx.Task()
    
    def start(self) -> None:
        self._task.start()
    
    def stop(self) -> None:
        self._task.stop()
    
    def close(self) -> None:
        self._task.close()
        
    def __getDeviceNames(self) -> list:
        sys = nidaqmx.system.System()
        return sys.devices.device_names


class NIDAQ_ai_task(NIDAQ_task):
    def __init__(self):
        """
        Constructor.
        
        Create an AI task
        """
        super().__init__()
        super().createTask()
        
    def createTask(self, port: str) -> None:
        super().stop()
        super().close()
        super().createTask()
        self._task.ai_channels.add_ai_voltage_chan(self._dev_name + "/" + port)
    
    def getAIData_single(self) -> list:
        """
        Obtain an analog input value.

        Returns:
            list: Analog input values.
        """
        try:
            return self._task.read(number_of_samples_per_channel=1)
        except nidaqmx.errors.DaqReadError:
            print('NIDAQ_ai_task: DaqReadError (getAIData_single)')
            return [False]
        
    def getAIData_multi(self, num: int) -> list:
        """
        Obtain an analog input value.

        Returns:
            list: Analog input values.
        """
        try:
            return self._task.read(number_of_samples_per_channel=num)
        except nidaqmx.errors.DaqReadError:
            print('NIDAQ_ai_task: DaqReadError (getAIData_multi)')
            return [False] * num
        

class NIDAQ_ao_task(NIDAQ_task):
    def __init__(self):
        """
        Constructor.
        
        Create an AO task
        """
        super().__init__()
        super().createTask()
    
    def createTask(self, port: str) -> None:
        super().stop()
        super().close()
        super().createTask()
        self._task.ao_channels.add_ao_voltage_chan(self._dev_name + "/" + port)
    
    def setAOData(self, data: float) -> None:
        """
        Set an analog output value.

        """
        try:
            self._task.write(data, auto_start=False)
        except nidaqmx.errors.DaqWriteError:
            print('NIDAQ_ao_task: DaqWriteError (setAOData)')


class NIDAQ_do_task(NIDAQ_task):
    def __init__(self):
        """
        Constructor.
        
        Create a DO task
        """
        super().__init__()
        super().createTask()
    
    def createTask(self, port: str, line: str) -> None:
        super().stop()
        super().close()
        super().createTask()
        self._task.do_channels.add_do_chan(self._dev_name + "/" + port + "/" + line, line_grouping=LineGrouping.CHAN_PER_LINE)
    
    def setDOData(self, data: bool) -> None:
        """
        Set a digital output value.

        """
        try:
            self._task.write(data, auto_start=False)
        except nidaqmx.errors.DaqWriteError:
            print('NIDAQ_do_task: DaqWriteError (setDOData)')