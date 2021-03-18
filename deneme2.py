import cv2
import os
import time
import numpy as np
from matplotlib import pyplot as plt
from picamera import PiCamera

cap = cv2.VideoCapture(0)

# Videoda olusturulan kutularin olcu degerleri
upper_left = (400, 50)
bottom_right = (575, 200)
upper_left1 = (75, 50)
bottom_right1 = (240, 200)

while True:
    # 16 farkli islem icin atanilan degiskenler
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    h = 0
    j = 0
    k = 0
    l = 0
    m = 0
    n = 0
    p = 0
    w = 0
    s = 0
    # Islem dogrulu icin 10 kere donen "for" dongusu
    for sayi in range(10):
        # Videonun okunmasi ve atanmasi
        _, frame = cap.read()

        # Video icinde iki kutunun cizilmesi ve cikartilmasi
        r = cv2.rectangle(frame, upper_left, bottom_right, (0, 255, 0), 1)
        rect_frame = frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]

        r1 = cv2.rectangle(frame, upper_left1, bottom_right1, (0, 255, 0), 1)
        rect_frame1 = frame[upper_left1[1]: bottom_right1[1], upper_left1[0]: bottom_right1[0]]

        # Kutularin icinin HSV'ye donusturulmesi
        hsv = cv2.cvtColor(rect_frame, cv2.COLOR_BGR2HSV)
        hsv1 = cv2.cvtColor(rect_frame1, cv2.COLOR_BGR2HSV)

        # El renginin daha net bulunmasi icin HSV degerleri
        tenrengi_MIN = np.array([0, 50, 40], np.uint8)
        tenrengi_MAX = np.array([255, 145, 255], np.uint8)

        # 2 kutu icin de ayri ayri yapilan Gauss Yumusatmasi, Threshold islemi ve arka plan cikarma islemleri
        gauss = cv2.GaussianBlur(hsv, (3, 3), 2)
        mask = cv2.inRange(gauss, tenrengi_MIN, tenrengi_MAX)

        result = cv2.bitwise_and(rect_frame, rect_frame, mask=mask)

        gauss1 = cv2.GaussianBlur(hsv1, (3, 3), 2)
        mask1 = cv2.inRange(gauss1, tenrengi_MIN, tenrengi_MAX)

        result1 = cv2.bitwise_and(rect_frame1, rect_frame1, mask=mask1)

        # 2 Kutu icin yapilan islemler sonrasi konturlama ve cizme islemi
        image, contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        img_copy = rect_frame.copy()
        final = cv2.drawContours(img_copy, contours, contourIdx=-1, color=(0, 0, 0), thickness=4)

        image1, contours1, hierarchy1 = cv2.findContours(image=mask1, mode=cv2.RETR_TREE,
                                                         method=cv2.CHAIN_APPROX_SIMPLE)
        contours1 = sorted(contours1, key=cv2.contourArea, reverse=True)
        img_copy1 = rect_frame1.copy()
        final1 = cv2.drawContours(img_copy1, contours1, contourIdx=-1, color=(0, 0, 0), thickness=4)

        # 1. kutu el alan ve cevre hesabi
        el_cevre = cv2.arcLength(contours[0], closed=True)
        el_alan = cv2.contourArea(contours[0])

        # 2. kutu el alan ve cevre hesabi
        el_cevre1 = cv2.arcLength(contours1[0], closed=True)
        el_alan1 = cv2.contourArea(contours1[0])

        # Toplam el alan ve cevre hesabi
        el_cevre2 = el_cevre + el_cevre1
        el_alan2 = el_alan + el_alan1

        # El alan ve cevrenin bastirilmasi
        print("Cekilen fotograf cevresi : ", el_cevre2)
        print("Cekilen fotograf alani : ", el_alan2)

        # Videonun canli gosterimi
        cv2.imshow("frame", frame)
        cv2.waitKey(1)

        # for dongusu oncesi atanan degerlerin, el alani ve cevresine gore guncellenmesi
        if (850 < el_cevre2 < 1000 and 5000 < el_alan2 < 5400):
            a += 1
        elif (1000 < el_cevre2 < 1150 and 5500 < el_alan2 < 5900):
            b += 1
        elif (1100 < el_cevre2 < 1250 and 6300 < el_alan2 < 6650):
            c += 1
        elif (1200 < el_cevre2 < 1350 and 6850 < el_alan2 < 7200):
            d += 1
        elif (1250 < el_cevre2 < 1450 and 7800 < el_alan2 < 8150):
            e += 1
        elif (1400 < el_cevre2 < 1600 and 8800 < el_alan2 < 9400):
            f += 1
        elif (1100 < el_cevre2 < 1400 and 13000 < el_alan2 < 15500):
            g += 1
        elif (1400 < el_cevre2 < 1800 and 13500 < el_alan2 < 15500):
            h += 1
        elif (1275 < el_cevre2 < 1400 and 14000 < el_alan2 < 17000):
            j += 1
        elif (1450 < el_cevre2 < 1600 and 16000 < el_alan2 < 18000):
            k += 1
        elif (550 < el_cevre2 < 800 and 9000 < el_alan2 < 11500):
            l += 1
        elif (1200 < el_cevre2 < 1350 and 7300 < el_alan2 < 7700):
            m += 1
        elif (850 < el_cevre2 < 1150 and 4200 < el_alan2 < 4950):
            n += 1
        elif (950 < el_cevre2 < 1150 and 8000 < el_alan2 < 8500):
            p += 1
        elif (950 < el_cevre2 < 1150 and 7200 < el_alan2 < 7800):
            w += 1
        else:
            s += 1

        # Guncel degerlere gore kontrol etme ve komut gonderme
        if (a > 9):
            x = 0
            print("El hareketi sonucu yapilan isaret : ", x)
            os.system("irsend SEND_ONCE Samsung_BN59-01175B KEY_0")
        elif (b > 9):
            x = 1
            print("El hareketi sonucu yapilan isaret : ", x)
            os.system("irsend SEND_ONCE Samsung_TV KEY_1")
        elif (c > 9):
            x = 2
            print("El hareketi sonucu yapilan isaret : ", x)
            os.system("irsend SEND_ONCE Samsung_TV KEY_2")
        elif (d > 9):
            x = 3
            print("El hareketi sonucu yapilan isaret : ", x)
            os.system("irsend SEND_ONCE Samsung_TV KEY_3")
        elif (e > 9):
            x = 4
            print("El hareketi sonucu yapilan isaret : ", x)
            os.system("irsend SEND_ONCE Samsung_TV KEY_4")
        elif (f > 9):
            x = 5
            print("El hareketi sonucu yapilan isaret : ", x)
            os.system("irsend SEND_ONCE Samsung_BN59-01175B KEY_5")
        elif (g > 9):
            x = 6
            print("El hareketi sonucu yapilan isaret : ", x)
            os.system("irsend SEND_ONCE Samsung_BN59-01175B KEY_6")
        elif (h > 9):
            x = 7
            print("El hareketi sonucu yapilan isaret : ", x)
            os.system("irsend SEND_ONCE Samsung_BN59-01175B KEY_7")
        elif (j > 9):
            x = 8
            print("El hareketi sonucu yapilan isaret : ", x)
            os.system("irsend SEND_ONCE Samsung_BN59-01175B KEY_8")
        elif (k > 9):
            x = 9
            print("El hareketi sonucu yapilan isaret : ", x)
            os.system("irsend SEND_ONCE Samsung_BN59-01175B KEY_9")
        elif (l > 9):
            print("El hareketi sonucu yapilan isaret : Ac / Kapat")
            os.system("irsend SEND_ONCE Samsung_BN59-01175B KEY_POWER")
        elif (m > 9):
            print("El hareketi sonucu yapilan isaret : Kanal Arttir")
            os.system("irsend SEND_ONCE Samsung_BN59-01175B KEY_10CHANNELSUP")
        elif (n > 9):
            print("El hareketi sonucu yapilan isaret : Kanal Azalt")
            os.system("irsend SEND_ONCE Samsung_BN59-01175B KEY_10CHANNELSDOWN")
        elif (p > 9):
            print("El hareketi sonucu yapilan isaret : Ses Arttir")
            os.system("irsend SEND_ONCE Samsung_BN59-01175B KEY_VOLUMEUP")
        elif (w > 9):
            print("El hareketi sonucu yapilan isaret : Ses Azalt")
            os.system("irsend SEND_ONCE Samsung_BN59-01175B KEY_VOLUMEDOWN")
        elif (s > 9):
            print("El bulunamadi.")