import os
import sys
#https://stackoverflow.com/questions/35507127/how-to-get-click-position-on-qpixmap
print("BU SORUNA BAK")
import designer_py_tik_testi
print("BU SORUNA BAK")
from PIL import Image
from PIL.ImageQt import ImageQt
from serial.tools import list_ports
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QMessageBox
from PyQt5 import uic
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor, QImage
from PIL import Image
import numpy
import serial
import time
import threading

g_measuring_val_3 = ":01R023;69F5\r\n"
make_highest_baud_rate = ":01W006;4;61FC\r\n"
make_baud_rate_921600 = ":01W006;3;51FE\r\n"
make_baud_rate_115200 = ":01W006;2;C1FF\r\n"
rs485_unlock = ":01W010;0;E9C3\r\n"
baud_rates = [38400, 57600, 115200, 921600, 1843200]
#imgemiz = np.zeros((300,250))

def serial_ports_arduino():
    ports = list(serial.tools.list_ports.comports())
    for port_no, description, address in ports:
        if 'LOCATION=1-1' in address:
            return port_no

def serial_ports_sensor():
    ports = list(serial.tools.list_ports.comports())
    for port_no, description, address in ports:
        if 'LOCATION=1-2' in address:
            return port_no

ser_sensor = serial.Serial(
    port=serial_ports_sensor(),
    baudrate=57600,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser_arduino = serial.Serial(
    port=serial_ports_arduino(),
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
print(ser_arduino.isOpen())
print(ser_arduino.name)
print(ser_sensor.isOpen())
print(ser_sensor.name)

#chekcking baud rate of the device
#and making the baud rate of the software the same as the device
for i in range(5):
    print(baud_rates[i])
    ser_sensor.baudrate = baud_rates[i]
    ser_sensor.write(rs485_unlock.encode('utf-8'))
    time.sleep(3)
    if(ser_sensor.inWaiting()):
        print("Sensörün Baud Oranı:")
        print(baud_rates[i])
        break

print("KONFİGÜRASYON")
for k in range(5):
    ser_sensor.write(g_measuring_val_3.encode('utf-8'))
    print(ser_sensor.readline())
print("KONFİGÜRASYON")

ser_sensor.write(make_baud_rate_921600.encode('utf-8'))
time.sleep(3)
ser_sensor.baudrate = 921600

print("2222____KONFİGÜRASYON____2222")
for k in range(5):
    ser_sensor.write(g_measuring_val_3.encode('utf-8'))
    print(ser_sensor.readline())
print("2222____KONFİGÜRASYON____2222")
data = []

def read_from_port(ser):
    while True:
        reading = ser.readline() #.decode(errors='replace')
        data.append(reading)

if_ici_sayac=0

while True:
    if (ser_arduino.read() == b'a'):
        ser_arduino.flushInput()
        ac = ser_sensor.write(g_measuring_val_3.encode('utf-8'))
        #time.sleep(0.02)
        if (ser_sensor.inWaiting()):
            data.append(ser_sensor.readline())
            print("evet")
        else:
            print("hayır")
            data.append(b':01A;0;0;-3000;0 ;9583\r\n')
        #time.sleep(0.02)
        print(if_ici_sayac)
        #thread = threading.Thread(target=read_from_port, args=(ser_sensor,))
        #thread.start()
        if_ici_sayac = if_ici_sayac + 1
    if (ser_arduino.read() == b'b'):
        ser_arduino.flushInput()
        print("ÇIKILIYOR")
        break

z_matrisi = numpy.zeros((if_ici_sayac, 227))    #tıklanılan yerin yükseklik bilgisini bu matristen elde edeceğiz,
                                              #  bu matris imge büyüklüğünde bir matris

print("IF  içi sayaç: %d" % if_ici_sayac)
im = Image.new('L', (227, if_ici_sayac))
im_pixels = im.load()
img_indis = 0

for g in range(len(data)):   #datanın satır sayısı
    en_data = data[g]        #datanın g. satırını komple en_data ya ata
    print(en_data)
    #data_bir = chr(data[15])
    #data_iki = chr(data[16])
    #data_toplam = data_bir + data_iki
    #data_t_n = int(data_toplam) + 5
    #print(data_t_n)
    data_tum = en_data[15:]   #data_tum artık tek boyutlu
    data_nihai = []
    sayi = ''
    print(data_tum)
    sayac = 0
    for i in range(len(data_tum)):    #veriler karakter olarak geldiği için onları sayılara çeviriyoruz
        if chr(data_tum[i]) == ';':
            for j in range(sayac,0,-1):
                sayi = sayi + chr(data_tum[i-j])
            try:
                data_nihai.append(int(sayi))
            except:
                data_nihai.append(0)
            sayac = 0
            sayi = ''
            break
        if chr(data_tum[i]) == ' ':
            for j in range(sayac,0,-1):
                sayi = sayi + chr(data_tum[i-j])
            try:
                data_nihai.append(int(sayi))
            except:
                data_nihai.append(0)
            sayac = 0
            sayi = ''
        else:
            sayac = sayac + 1
    x_uzunluk = []
    z_uzunluk = []
    data_nihai = data_nihai[1:]
    for i in range(len(data_nihai)):
        if i % 2 == 0:
            x_uzunluk.append((data_nihai[i]))
        else:
            z_uzunluk.append((data_nihai[i]))
    onceki_c = 0
    anlik_c = 0
    anlik_cx = 0
    onceki_cx = 0
    for k in range(len(z_uzunluk)):
        if k % 2 == 0:
            onceki_c = (x_uzunluk[k])/100 #mm ye çevirdik
            onceki_cx = onceki_c*3.78   #pixele çevirdik
        else:
            anlik_c = (x_uzunluk[k])/100 #mm ye çevirdik
            anlik_cx = anlik_c*3.78   #pixele çevirdik
            if (anlik_c - onceki_c)<=0.3:
                for j in range(round(onceki_cx), round(anlik_cx)+1):
                    im_pixels[j,img_indis] = round((z_uzunluk[k]*256)/5000)
                    z_matrisi[img_indis][j] = (z_uzunluk[k]/100) + 50
    img_indis = img_indis + 1

print("IMGE OLUŞTURULDU")

#http://pythondanotlarim.blogspot.com/2015/09/python3-programlar-exeye-cevirmek-ve.html
#https://stackoverflow.com/questions/38977929/pyinstaller-creating-exe-runtimeerror-maximum-recursion-depth-exceeded-while-ca    

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


# baseUI = os.path.join(RESOURCE_PATH, "MainGui.ui")
baseUI = resource_path("laser_gui_tik_testi.ui")
baseUIClass, baseUIWidget = uic.loadUiType(baseUI)

class Logic(baseUIWidget, baseUIClass):

    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        #self.img = QImage('logo.png')
        #pixmap = QPixmap(QPixmap.fromImage(self.img))
        pixmap = QPixmap('logo.png')
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        global pixmap3
        self.pixels = self.get_pixel() #get_pixel fonksiyonunun döndürdüğü pix numpy dizisini pixelse atıyoruz
        image = QImage(self.pixels , im.size[0], im.size[1], QImage.Format_RGB32)

        # gama değeri ile konstrast germe
        gama = 2
        invGama = 1.0 / gama
        for g in range(227):
            for j in range(if_ici_sayac):
                k = image.pixel(g, j)
                a = QColor(k).getRgb()[2]
                image.setPixel(g, j, QColor(int(((a / 255) ** invGama) * 255), int(((a / 255) ** invGama) * 255),int(((a / 255) ** invGama) * 255)).rgb())

        pixmap3 = QPixmap.fromImage(image)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 50, 227, if_ici_sayac))
        self.label_3.setPixmap(pixmap3)
        self.resize(pixmap3.width(), pixmap3.height())

        #self.get_pixel()
        #pixmap2 = QPixmap(500,500)          #QPixmap(500,500)
        #self.label_2.setPixmap(pixmap2)
        #self.resize(pixmap2.width(), pixmap2.height())

        self.pushButton1.clicked.connect(self.btn_1_Clicked) #resetle
        self.pushButton2.clicked.connect(self.btn_2_Clicked) #çizdir

        self.show()

    def btn_2_Clicked(self):
        self.pushButton1.setEnabled(True)
        self.pushButton2.setEnabled(False)

    def btn_1_Clicked(self):
        self.pushButton1.setEnabled(False)
        self.pushButton2.setEnabled(True)

    def get_pixel(self):
        #im = Image.open('nihai_goruntu_sensor_baudrate_921600_bant_yavas.jpg', 'r')
        width, height = im.size
        global channels
        pix = list(im.getdata())
        if im.mode == 'RGB':
            print('RGB')
            channels = 3
        elif im.mode == 'L':
            channels = 1
            print('L')
        else:
            print('unknown mode', im.mode)
            channels = None
        pix = numpy.array(pix).reshape((width, height, channels))
        return pix

    def mousePressEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        x = pos.x()
        y = pos.y()
        x = int(x-60)  #imgenin başlangıç noktaları
        y = int(y-50)
        global channels
        if (x>=0 and x<228) and (y>=0 and y<(if_ici_sayac)):
            try:
                k = z_matrisi[y][x]
                #global pixmap3
                #img = pixmap3.toImage()
                #k = img.pixel(x, y)
                print(k)
                #print(QColor(k).getRgb())
                QMessageBox.information(self, "Profil olcum", "Yukseklik degeri:  %f mm" % k)
                #QMessageBox.information(self, "Pixel Degerleri","R:%d" % QColor(k).getRgb()[0] + "  G:%d" % QColor(k).getRgb()[1] + "  B:%d" %QColor(k).getRgb()[2])
                #k = self.pixels[x,y] #self.pixels[x][y]
                #print(k)  #ana pencere üzerindeki her x, y değerinin pixel değerini yazıyor
                #if channels==3:
                #    QMessageBox.information(self, "Pixel Degerleri","R:%d" % k[0] + "  G:%d" % k[1] + "  B:%d" % k[2])
                #else:
                #    QMessageBox.information(self,  "Pixel Degeri", "%d" % k)
            except:
                print('failed to get pixels')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Logic(MainWindow)
    ui.showMaximized()
    sys.exit(app.exec_())