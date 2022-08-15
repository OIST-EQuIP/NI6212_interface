import nidaqmx

class NIDaqmx:
    def __init__(self,dev_name):
        self.dev = dev_name

    def getInputData(self,port):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(self.dev + "/" + port)
            return task.read(number_of_samples_per_channel=1)
        # print(self.port)
        
    def setOutputData(self,port,data):
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan(self.dev + "/" + port)
            task.write([data], auto_start=True)