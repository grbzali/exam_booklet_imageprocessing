import cv2
import numpy as np

def cevap_oku_fark2(image1, temp1, image2, temp2):
    gelen = [image1, temp1, image2, temp2]

    kernel = np.ones((3, 3), np.uint8)  # kalıntılara uygulanacak dilasyon için 3x3 boyutunda birim matris oluşturuldu
    temp_say_siyah = 0
    x = 0
    secim = []  # şıkları karşılaştırmak için seçim dizisi oluşturuldu
    while x < len(gelen):

        fark = cv2.addWeighted(gelen[x], 0.8, gelen[x + 1], 0.2, 0)  # işaretli şık işaretlenmemiş şıkkın üzerinde saydam bir şekilde yerleştiriliyor

        fark[np.where((fark <= [20, 20, 20]).all(axis=2))] = [255, 255, 255]  # siyah olan pikseller siliniyor

        fark = cv2.dilate(fark, kernel, iterations=1)  # kalıntılara dilasyon uygulanıyor

        fark = cv2.cvtColor(fark, cv2.COLOR_BGR2GRAY)  # çıkan fark görüntüsü yani işaret gri tona çeviriliyor
        ret, fark = cv2.threshold(fark, 200, 255, cv2.THRESH_BINARY)  # saydam görüntü siyah tona çevirilmesi için binary tabana çeviriliyor

        px = fark  # fark matrisi px değişkenine atanıyor
        say_siyah = 0  # siyah pixel saydırmak için sayaç tutuluyor
        for k in range(0, 70):
            for t in range(0, 150):
                if px[k][t] == 0:
                    say_siyah += 1  # siyah pixeller sayılıyor
        secim.append(say_siyah)  # hesaplanan siyah pikseller seçim dizisine atanıyor

        x += 2

    fark = secim[0] - secim[1]  # gelen iki şıkkın işaret piksel farkı bulunuyor
    print(secim)
    if fark > 0:  # belirlenen eşiğin üstünde olan doğru şık olarak return ediliyor
        return 0
    else:
        return 1

def cevap_oku_fark3(image1, temp1, image2, temp2, image3, temps3):
    gelen = [image1, temp1, image2, temp2, image3, temps3]

    kernel = np.ones((3, 3), np.uint8)  # kalıntılara uygulanacak dilasyon için 3x3 boyutunda birim matris oluşturuldu
    temp_say_siyah = 0
    x = 0
    secim = []  # şıkları karşılaştırmak için seçim dizisi oluşturuldu
    while x < len(gelen):

        fark = cv2.addWeighted(gelen[x], 0.7, gelen[x + 1], 0.3, 0)  # işaretli şık işaretlenmemiş şıkkın üzerinde saydam bir şekilde yerleştiriliyor

        fark[np.where((fark <= [20, 20, 20]).all(axis=2))] = [255, 255, 255]  # siyah olan pikseller siliniyor

        fark = cv2.dilate(fark, kernel, iterations=1)  # kalıntılara dilasyon uygulanıyor

        fark = cv2.cvtColor(fark, cv2.COLOR_BGR2GRAY)  # çıkan fark görüntüsü yani işaret gri tona çeviriliyor
        ret, fark = cv2.threshold(fark, 200, 255, cv2.THRESH_BINARY)  # saydam görüntü siyah tona çevirilmesi için binary tabana çeviriliyor

        px = fark  # fark matrisi px değişkenine atanıyor
        say_siyah = 0  # siyah pixel saydırmak için sayaç tutuluyor

        for k in range(0, 70):
            for t in range(0, 150):
                if px[k][t] == 0:
                    say_siyah += 1  # siyah pixeller sayılıyo
        secim.append(say_siyah)  # hesaplanan siyah pikseller seçim dizisine atanıyor
        x += 2
    print("secim dizisi", secim)
    fark = secim[0] - secim[1]# gelen iki şıkkın işaret piksel farkı bulunuyor
    fark2 = secim[0] - secim[2]

    if fark > 50 and fark2 > 50:  # belirlenen eşiğin üstünde olan doğru şık olarak return ediliyor
        return 0
    else:
        return 1
