import cv2
import numpy as np
import json
from iki_cevap_fark import cevap_oku_fark
import time
start_time = int(round(time.time() * 1000))

A_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\temps\\A.png')
ret, A_temp1 = cv2.threshold(A_temp1, 200, 255, cv2.THRESH_BINARY)
B_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\temps\\B.png')
ret, B_temp1 = cv2.threshold(B_temp1, 200, 255, cv2.THRESH_BINARY)
C_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\temps\\C.png')
ret, C_temp1 = cv2.threshold(C_temp1, 200, 255, cv2.THRESH_BINARY)
D_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\temps\\D.png')
ret, D_temp1 = cv2.threshold(D_temp1, 200, 255, cv2.THRESH_BINARY)

temps1 = [A_temp1, B_temp1, C_temp1, D_temp1]

sk = []
sk1 = []
dogru_sk = []

def main(image1, image2, s, coords):


    sorular = coords["sorular"]
    print("KİTAPÇIK NO:", s)
    img_rgb = image1  # işaretli görüntü
    img_gray = image2  # ham görüntü
    birden_fazla = []
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)  # ham görüntünün gri tona çevirilmesi
    ret, thresh2 = cv2.threshold(img_rgb, 200, 255, cv2.THRESH_BINARY)  # ham görüntünün binary tabana çevirilmesi
    ret, thresh3 = cv2.threshold(img_rgb, 200, 255, cv2.THRESH_BINARY)  # iki şık ve fazla işaret saptandığında bu görüntüden kırpılıp gönderiliyor fark metoduna

    soru_say = len(sorular)
    sk_say = (soru_say) * 4
    koordinat_sk = []
    koordinat_sk1 = []

    for i in range(len(coords["sorular"])):
        for sklar in coords["sorular"][i]:
            sk.append(thresh2[int((sorular[i][sklar]["center"]["first"]["y"])):int((sorular[i][sklar]["center"]["second"]["y"])),
                                int((sorular[i][sklar]["center"]["first"]["x"]))-50:int((sorular[i][sklar]["center"]["second"]["x"]))])#şıkların hepsi tek tek verilen 2 nokta ile sk[a,b,c,d,a,b,c,d] olarak alındı.
            sk1.append(thresh3[int((sorular[i][sklar]["center"]["first"]["y"])):int((sorular[i][sklar]["center"]["second"]["y"])),
                                int((sorular[i][sklar]["center"]["first"]["x"]))-50:int((sorular[i][sklar]["center"]["second"]["x"]))])#coklu cevaplar için aynı şekilde sıklar sk1 e alındı.
            koordinat_sk.append((int((sorular[i][sklar]["center"]["first"]["x"]))-50, int((sorular[i][sklar]["center"]["first"]["y"])))) #rectangle kullanmak için şıkların ilk koordinatları alndı
            koordinat_sk1.append((int((sorular[i][sklar]["center"]["second"]["x"])), int((sorular[i][sklar]["center"]["second"]["y"])))) #rectangle kullanmak için şıkların ikinci koordinatları alndı
    cv2.imwrite('C:\\Users\\NovaPM\\Desktop\\adogru_cevap.png', sk[0])
    cv2.imwrite('C:\\Users\\NovaPM\\Desktop\\bdogru_cevap.png', sk[1])
    cv2.imwrite('C:\\Users\\NovaPM\\Desktop\\cdogru_cevap.png', sk[2])
    cv2.imwrite('C:\\Users\\NovaPM\\Desktop\\ddogru_cevap.png', sk[3])

    i = 0
    while i < sk_say:
        j = i % 4   #şık sayısı ilk 4 den sonra hangi şık oldugunu tutuyoruz.
        fark = sk[i] #sk içinde olan şıklar tek tek alınıyor

        fark = cv2.cvtColor(fark, cv2.COLOR_BGR2GRAY)  # görüntü gray tona çeviriliyor
        ret, fark = cv2.threshold(fark, 200, 255, cv2.THRESH_BINARY)

        fark1 = temps1[j] #mevcut şıkkın ham frame i alınıyor
        fark1 = cv2.cvtColor(fark1, cv2.COLOR_BGR2GRAY)  # görüntü gray tona çeviriliyor
        ret, fark1 = cv2.threshold(fark1, 200, 255, cv2.THRESH_BINARY)

        '''
        im = cv2.resize(fark, None, fx=8, fy=8, interpolation=cv2.INTER_CUBIC)
        im1 = cv2.resize(fark1, None, fx=8, fy=8, interpolation=cv2.INTER_CUBIC)
        cv2.imshow("",im)
        cv2.waitKey()
        cv2.imshow("", im1)
        cv2.waitKey()
        '''
        px = fark  # fark px matrisi px değişkenine iletiliyor
        px1 = fark1
        say_fark = 0  # siyah pixel saydırmak için sayaç tutuluyor
        say_fark1 = 0

        for k in range(0, 70):
            for t in range(0, 150):
                if px[k][t] == 0:
                    say_fark += 1  # siyah pixeller sayılıyor

        for k in range(0, 70):
            for t in range(0, 150):
                if px1[k][t] == 0:
                    say_fark1 += 1  # siyah pixeller sayılıyor

        siyah_fark = abs(say_fark1 - say_fark)

        print(i, ". sık ", say_fark1)
        print(i, ". sık ", say_fark)
        print(i, ". sık ", siyah_fark)

        if siyah_fark > 250:
            if len(birden_fazla) != int(i / 4) + 1:
                birden_fazla.append(int(i / 4) + 1)

                print(int(i / 4) + 1, ". sorunun ", int(j + 1), ". şıkkı-->farkı", siyah_fark)
                if j == 0:
                    dogru_sk.append("A")
                elif j == 1:
                    dogru_sk.append("B")
                elif j == 2:
                    dogru_sk.append("C")
                else:
                    dogru_sk.append("D")
                cv2.rectangle(thresh2, (koordinat_sk[i][0], koordinat_sk[i][1]), ((koordinat_sk1[i][0]), (koordinat_sk1[i][1])), (0, 255, 0), 5)
            else:
                x = cevap_oku_fark(sk1[i - 1], temps1[j - 1], sk1[i], temps1[j])
                if x == 1:
                    dogru_sk.pop(len(dogru_sk) - 1)
                    if j == 0:
                        dogru_sk.append("A")
                    elif j == 1:
                        dogru_sk.append("B")
                    elif j == 2:
                        dogru_sk.append("C")
                    else:
                        dogru_sk.append("D")
                    cv2.rectangle(thresh2, (koordinat_sk[i - 1][0], koordinat_sk[i - 1][1]),
                                  ((koordinat_sk1[i - 1][0]), (koordinat_sk1[i - 1][1])), (0, 0, 255), 5)
                    cv2.rectangle(thresh2, (koordinat_sk[i][0], koordinat_sk[i][1]),
                                  ((koordinat_sk1[i][0]), (koordinat_sk1[i][1])), (0, 255, 0), 5)
                else:
                    dogru_sk.pop(len(dogru_sk) - 1)
                    j -= 1
                    if j == 0:
                        dogru_sk.append("A")
                    elif j == 1:
                        dogru_sk.append("B")
                    elif j == 2:
                        dogru_sk.append("C")
                    else:
                        dogru_sk.append("D")

                    cv2.rectangle(thresh2, (koordinat_sk[i - 1][0], koordinat_sk[i - 1][1]),
                                  ((koordinat_sk1[i - 1][0]), (koordinat_sk1[i - 1][1])), (0, 255, 0), 5)
                    cv2.rectangle(thresh2, (koordinat_sk[i][0], koordinat_sk[i][1]),
                                  ((koordinat_sk1[i][0]), (koordinat_sk1[i][1])), (0, 0, 255), 5)

        else:
            cv2.rectangle(thresh2, (koordinat_sk[i][0], koordinat_sk[i][1]),
                          ((koordinat_sk1[i][0]), (koordinat_sk1[i][1])), (0, 0, 255), 5)
        i += 1

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("-------------------------------------------------------")
    print(birden_fazla)
    print("-------------------------------------------------------")
    cv2.imwrite('C:\\Users\\NovaPM\\Desktop\\' + str(s) + '_dogru_cevap.png', thresh2)
    finish_time = int(round(time.time() * 1000))
    print("Sistem Çalışma Süresi:", (finish_time) - (start_time), "Ms")

    return dogru_sk

