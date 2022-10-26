# NI6212_interface
![GitHub watchers](https://img.shields.io/github/watchers/OIST-EQuIP/NI6212_interface?style=social)
![Python](https://img.shields.io/badge/python-v3.9.12-007396.svg?logo=python&style=popout)
![PyQt5](https://img.shields.io/badge/PyQt5-v5.15.7-007396.svg?logo=python&style=popout)
![pyqtgraph](https://img.shields.io/badge/pyqtgraph-v0.12.4-007396.svg?logo=python&style=popout)
![pglive](https://img.shields.io/badge/pglive-v0.3.3-007396.svg?logo=python&style=popout)
![nidaqmx](https://img.shields.io/badge/nidaqmx-v0.6.3-44A833.svg?style=popout)

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

There are three tabs on the application: "Analog Input", "Analog Output" and "Digital Output".

### Analog Input

![image](https://github.com/OIST-EQuIP/NI6212_interface/blob/main/img/AI.PNG)

"Analog Input" measures the voltage on the channel selected in the drop-down list.
To start measurement, press the "START" button. To exit, press the button labeled "STOP". "Analog Input" can detect -5.4 to 5.4v.

### Analog Output

![image](https://github.com/OIST-EQuIP/NI6212_interface/blob/main/img/AO.PNG)

"Analog Output" outputs the specified voltage to the channel selected in the drop-down list.
Specifiable Output values are from -10 to 10.

### Digital Output

![image](https://github.com/OIST-EQuIP/NI6212_interface/blob/main/img/DO.PNG)

Under "Digital Output," voltage flows to the line of the port selected in the drop-down list.
Press the "START" button to start measurement, and press the "Set True" button to output the signal. Pressing the "Set False" button stops signal output.

## Reference
[PyQt5 document](https://pythonspot.com/pyqt5/)

[NI-DAQmx Python API](https://nidaqmx-python.readthedocs.io/en/latest/)