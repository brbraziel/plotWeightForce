# Plot Weight Force

This is a Python UI to collect and visualize received data. It was programmed to receive information from a serial port _(/dev/ttyACM0)_ and make instant plots (using Threads) about weight force. At the end of execution, is exported a .csv file contained all the acquired data.

### What to install
In this project I used the following libraries:

- PyQt4
- MatPlotLib 
- Pandas
- matplotlib.backends.backend_qt4agg

### Run 
After installing all the required libraries, you need to plug in your data receptor (such as arduino) in the USB port that corresponds to _ttyACM0_. If you want to use another port make sure to change the arduinoData variable in order to communicate with your chosen one.
Afterwards you can run this file using:

```
python rocketPlots.py
```

### Using
When clicking on "Iniciar Leitura" the project will collect the data and show in real time in a chart. 
When you finish your collection, you can click on "Finalizar Leitura". The program will export a .csv file in the same folder you opened your terminal and will close automatically.
