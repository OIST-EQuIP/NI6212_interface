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

There are three tabs on the application: "Analog Input", "Analog Output", "Digital Output", and 'Scan Amplitude".

![image](https://github.com/OIST-EQuIP/NI6212_interface/blob/main/img/AI.PNG)

"Analog Input" measures the voltage on the channel selected in the drop-down list.
To start measurement, press the "START" button. To exit, press the button labeled "STOP". "Analog Input" can detect -5.4 to 5.4v.

![image](https://github.com/OIST-EQuIP/NI6212_interface/blob/main/img/AO.PNG)

"Analog Output" outputs the specified voltage to the channel selected in the drop-down list.
Specifiable Output values are from -10 to 10.

![image](https://github.com/OIST-EQuIP/NI6212_interface/blob/main/img/DO.PNG)

In "Digital Output", voltage flows to the channel selected by the check box.
Press the "START" button to start measurement, and press the "ON" button to output the signal. Pressing the "OFF" button stops signal output.

![image](https://github.com/OIST-EQuIP/NI6212_interface/blob/main/img/SA.PNG)

"Scan Amplitude" sets the threshold value and performs the scanning operation.
The analog output is gradually increased until the analog input reaches the threshold value.
When the analog input reaches the threshold value, the analog output stops increasing or decreasing and a digital signal is output.

Enter a threshold value in the "Threshold" field.
"vmax" and "vmin" are set to the maximum and minimum values that the USB-6212 can detect on the analog input.
"vamp" allows you to set the amplitude height.
"step size" allows you to set the amplitude increase/decrease value.
With "dt", you can set the output wait time for the digital signal to be output after the threshold value is detected.
"AO Channel", "AI Channel", and "DI Port/Channel" allow you to select the port and channel to be used.

The device name can be edited by pressing the "Edit" button.
If the device name is different from the default value, please change it here.

If the behavior is not correct, you can initialize it with the "Init" button. It is recommended to stop all operations before pressing the "Init" button.

## Reference
[PyQt5 document](https://pythonspot.com/pyqt5/)

[NI-DAQmx Python API](https://nidaqmx-python.readthedocs.io/en/latest/)