import os
import sys

print("BU SORUNA BAK")
import designer_py
print("BU SORUNA BAK")
import serial
from PIL import Image
from serial.tools import list_ports
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor
import numpy as np

imgemiz = np.zeros((300,250))
g_measuring_val_3 = ":01R023;69F5\r\n"
print(g_measuring_val_3.encode('utf-8'))

#http://pythondanotlarim.blogspot.com/2015/09/python3-programlar-exeye-cevirmek-ve.html
#https://stackoverflow.com/questions/38977929/pyinstaller-creating-exe-runtimeerror-maximum-recursion-depth-exceeded-while-ca    
def serial_ports():
    # produce a list of all serial ports. The list contains a tuple with the port number,
    # description and hardware address
    #
    ports = list(serial.tools.list_ports.comports())

    # return the port if 'USB' is in the description
    for port_no, description, address in ports:
        if 'USB' in description:
            return port_no
ser = serial.Serial(
    port=serial_ports(),
    baudrate=57600,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

##RS485 KİLİDİNİ AÇMAYI UNUTMA

# Define function to import external files when using PyInstaller.
def resource_path(relative_path): # FOR ICON
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Here you can add your ui path from designer, no need to convert
# RESOURCE_PATH = r"E:\Prj\Yongatek\FishCounterOpenCV\FishCounter11"
# baseUI = os.path.join(RESOURCE_PATH, "MainGui.ui")
baseUI = resource_path("laser_gui.ui")
baseUIClass, baseUIWidget = uic.loadUiType(baseUI)


class Logic(baseUIWidget, baseUIClass):

    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(30, 20, 251, 151))

        pixmap = QPixmap('logo.png')
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        #image = pixmap.toImage()



        pixmap2 = QPixmap(500,500)          #QPixmap(500,500)
        self.label_2.setPixmap(pixmap2)
        #self.resize(pixmap2.width(), pixmap2.height())



        def btn_2_Clicked():
            self.pushButton1.setEnabled(True)
            self.pushButton2.setEnabled(False)
            data = []
            ac = ser.write(g_measuring_val_3.encode('utf-8'))
            # print(ac)

            data = ser.readline()
            print(data)
            # data_bir = chr(data[15])
            # data_iki = chr(data[16])
            # data_toplam = data_bir + data_iki
            # data_t_n = int(data_toplam) + 5
            # print(data_t_n)
            data_tum = data[15:]
            data_nihai = []
            sayi = ''
            print(data_tum)
            sayac = 0
            for i in range(len(data_tum)):
                if chr(data_tum[i]) == ';':
                    for j in range(sayac, 0, -1):
                        sayi = sayi + chr(data_tum[i - j])
                    data_nihai.append(int(sayi))
                    sayac = 0
                    sayi = ''
                    break
                if chr(data_tum[i]) == ' ':
                    for j in range(sayac, 0, -1):
                        sayi = sayi + chr(data_tum[i - j])
                    data_nihai.append(int(sayi))
                    sayac = 0
                    sayi = ''
                else:
                    sayac = sayac + 1
            x_uzunluk = []
            z_uzunluk = []
            data_nihai = data_nihai[1:]
            for i in range(len(data_nihai)):
                if i % 2 == 0:
                    x_uzunluk.append(data_nihai[i])
                else:
                    z_uzunluk.append(data_nihai[i])

            gv = self.graphicsView
            for item in gv.items():
                gv.removeItem(item)
            self.graphicsView.plot(z_uzunluk)

        #self.pushButton1.clicked.connect(btn_1_Clicked) #resetle
        self.pushButton2.clicked.connect(btn_2_Clicked) #çizdir


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Logic(MainWindow)
    ui.showMaximized()
    sys.exit(app.exec_())