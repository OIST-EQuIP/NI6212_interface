# NI6212_interface

![image](https://github.com/OIST-EQuIP/NI6212_interface/blob/main/img/Capture.PNG)

This is a GUI application developed for NATIONAL INSTRUMENTS' NI USB-6212 BNC BUS-POWERED M SE.

Analog input/output of voltage and digital output can be performed.

## Requirement
- Windows10
- Python 3.9.12
- PyQt5 5.15.7
- pyqtgraph 0.12.4
- pglive 0.3.3
- nidaqmx 0.6.3

## Usage
To run this application, run src/App.py.

```
$ cd src

$ python App.py
```

## Description

There are three tabs on the application: "Analog Input," "Analog Output," and "Digital Output".

![image](https://github.com/OIST-EQuIP/NI6212_interface/blob/main/img/AI.PNG)

"Analog Input" measures the voltage on the channel selected in the drop-down list.
To start measurement, press the "START" button. To exit, press the button labeled "STOP".

![image](https://github.com/OIST-EQuIP/NI6212_interface/blob/main/img/AO.PNG)

"Analog Output" outputs the specified voltage to the channel selected in the drop-down list.
Specifiable Output values are from -10 to 10.

![image](https://github.com/OIST-EQuIP/NI6212_interface/blob/main/img/DO.PNG)

In "Digital Output", voltage flows to the channel selected by the check box.
Press the "START" button to start measurement, and press the "ON" button to output the signal. Pressing the "OFF" button stops signal output.

The device name can be edited by pressing the "Edit" button.
If the device name is different from the default value, please change it here.

## Reference
[PyQt5 document](https://pythonspot.com/pyqt5/)

[NI-DAQmx Python API](https://nidaqmx-python.readthedocs.io/en/latest/)