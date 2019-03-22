from PyQt4.uic import loadUiType
from PyQt4 import QtCore, QtGui, uic
import random
import os
import threading
import calendar
import matplotlib.pyplot as plt
import numpy as np
import serial
import time
import pandas as pd
from datetime import datetime
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

Ui_MainWindow, QMainWindow = loadUiType('rocketv3.ui')

class acquisitionTask(threading.Thread):

    def __init__(self, janela_principal):
        acquisitionTask.ligado = True
        threading.Thread.__init__(self)
        self.janela_principal = janela_principal
        self.setDaemon(True)
        self.desligado = threading.Event()

    def run(self):
        while not self.desligado.is_set():
            try:
                #time.sleep(0.1)
                arduinoData = serial.Serial("/dev/ttyACM0", 115200).close()
                arduinoData = serial.Serial("/dev/ttyACM0", 115200)
                arduinoString = arduinoData.readline()
                empuxo = float(arduinoString)/18.83896834622
                self.janela_principal.update(empuxo)
            except:
                pass


class Main(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setStyleSheet('font-size: 12pt;')  # ' font-family: Courier;')
        self.setupUi(self)
        self.valueTime.setText("0 secs")
        self.valueEmpuxo.setText("0 m")
        self.startStopButton.setText("Iniciar Leitura")
        self.startStopButton.clicked.connect(self.iniciar)
        self.dados_task = acquisitionTask(self)

        # Canvas e Toolbar
        self.figure = plt.figure(figsize=(15, 5))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.framePlot.addWidget(self.canvas, 1, 0, 1, 2)
        self.framePlot.addWidget(self.toolbar, 2, 0, 1, 2)

        # dados
        self.tempos=[]
        self.empuxos=[]
        

    def update(self, empuxo):
        tempo = time.time() - self.time0
        self.tempos.append(tempo)
        self.empuxos.append(empuxo)
        self.ax.clear()
        self.valueEmpuxo.setText("{} g".format(empuxo))
        self.valueTime.setText("{} secs".format(tempo))
        self.ax.plot(self.tempos, self.empuxos,'o')
        self.ax.plot(self.tempos, self.empuxos)
        self.canvas.draw()
        print(empuxo, tempo)

    def iniciar(self):
        plt.ion()
        self.startStopButton.setText("Finalizar Leitura")
        self.startStopButton.clicked.disconnect()
        self.startStopButton.clicked.connect(self.parar)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('Peso')
        self.time0 = time.time()
        try:
            self.dados_task.start()
        except RuntimeError:
            pass

    def parar(self):
        plt.ioff()
        df = pd.DataFrame({"tempos" : self.tempos, "pesos" : self.empuxos})
        data = datetime.now()
        data = data.strftime("%H-%M-%S")
        data = str(data)+".csv"
        df.to_csv(data, index=False)
        self.dados_task.desligado.set()
        self.startStopButton.setText("Iniciar Leitura")
        self.startStopButton.clicked.connect(self.iniciar)

if __name__ == '__main__':
    import sys
    arduinoData = serial.Serial("/dev/ttyACM0", 115200).close()
    arduinoData = serial.Serial("/dev/ttyACM0", 115200)
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())