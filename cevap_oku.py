import cv2
import numpy as np

def cevap_oku(image1, image2, kitapcik, coords):


    dogru_sk = []
    s = kitapcik
    img_rgb = image1  # işaretli görüntü
    img_gray = image2  # ham görüntü

    birden_fazla = []
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)  # ham görüntünün gri tona çevirilmesi
    ret, thresh2 = cv2.threshold(img_rgb, 200, 255, cv2.THRESH_BINARY)  # ham görüntünün binary tabana çevirilmesi
    ret, thresh3 = cv2.threshold(img_rgb, 200, 255, cv2.THRESH_BINARY)  # iki şık ve fazla işaret saptandığında bu görüntüden kırpılıp gönderiliyor fark metoduna

    A_temp = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\A.png', 0)  # ham görüntü üzerinde şıkların koordinatlarını bulmak için şıkların frame'lerinin gri tonda yüklenmesi
    B_temp = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\B.png', 0)
    C_temp = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\C.png', 0)
    D_temp = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\D.png', 0)

    Dogru_temp = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\Dogru.png', 0)  # doğru yanlış şıklarının koordinatları için frame'lerin yüklenmesi
    Yanlis_temp = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\Yanlis.png', 0)
    isaret_temp = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\isaret.png', 0)  # işaretli işaretsiz piksel farkı için ham görüntüdeki işaretlenecek bölgenin frame'i yüklendi

    A_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\A.png')
    ret, A_temp1 = cv2.threshold(A_temp1, 200, 255, cv2.THRESH_BINARY)
    B_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\B.png')
    ret, B_temp1 = cv2.threshold(B_temp1, 200, 255, cv2.THRESH_BINARY)
    C_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\C.png')
    ret, C_temp1 = cv2.threshold(C_temp1, 200, 255, cv2.THRESH_BINARY)
    D_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\D.png')
    ret, D_temp1 = cv2.threshold(D_temp1, 200, 255, cv2.THRESH_BINARY)

    pos_sk = []  # şıkların pozisyonlarının tutulacağı dizi
    pos_DY = []  # doğru-yanlışların pozisyonlarının tutulacağı dizi

    koordinat_sk = []  # şık koordinatlarının ABCD sırasıyla tutulacağı dizi
    koordinat_dy = []  # doğru-yanlış sırasıyla tutulacağı dizi

    sk = []  # kesilmiş şık frame'lerinin tutulacağı dizi
    sk1 = []  # ""
    dy = []  # kesilmiş doğru yanlış frame'lerinin tutulacağı dizi

    tempDY = [Dogru_temp, Yanlis_temp]  # ham doğru-yanlış frame'lerinin tutulacağı dizi

    temps = [A_temp, B_temp, C_temp, D_temp]  # ham ABCD'nin gri tonda tutulacağı dizi
    temps1 = [A_temp1, B_temp1, C_temp1, D_temp1]  # ham ABCD'nin binary tabanda tutulacağı dizi

    # -----------------------Doğru yanlış sorularının okunması için yapılan işlemler-------------------------------------------------------------------------------------------------
    for i in range(0, len(tempDY)):
        resDY = cv2.matchTemplate(img_gray, tempDY[i], cv2.TM_CCOEFF_NORMED)  # ham görüntü üzerinde doğru-yanlış frame'lerinin koordinatlarının bulunması
        threshold = 0.8  # görüntüdeki bozulmalara karşı eşleşme eşik değerinin bulunması
        loc = np.where(resDY >= threshold)  # eşik değerinden yüksek olan lokasyonların saptanması
        ptDY = []  # Doğru yanlış şıklarının pozisyonlarının tutulacağı dizi
        for ptDY in zip(*loc[::-1]):
            if len(pos_DY) == 0:
                pos_DY.append(ptDY)
            else:  # lokasyonların uzaklıklarının hesaplanması
                a = ptDY[0] - pos_DY[len(pos_DY) - 1][0]
                b = ptDY[1] - pos_DY[len(pos_DY) - 1][1]
                a = a * a
                b = b * b
                m = math.sqrt(a + b)
                if m < 10:  # birden fazla lokasyon geliyor birbirne yakım olan lokasyonlar tutulmuyor
                    continue
                else:
                    pos_DY.append(ptDY)  # uzak olan lokasyonlar diziye ekleniyor

    dy_say = len(pos_DY)
    soru_say_dy = (dy_say) // 2
    print("dy_say--->", dy_say, "soru_say_dy--->", soru_say_dy, "pos_DY--->", pos_DY)
    j = 0
    i = 0
    while i < soru_say_dy:
        j = i
        while j < dy_say:
            koordinat_dy.append(pos_DY[j])
            j += (soru_say_dy)
        i += 1
    for i in range(0, len(koordinat_dy)):
        dy.append(thresh2[(koordinat_dy[i][1]) + 10:(koordinat_dy[i][1]) + 60, (koordinat_dy[i][0]) + 184: (koordinat_dy[i][0]) + 244])

    i = 0
    while i < dy_say:
        j = i % 2
        fark = dy[i]

        fark = cv2.cvtColor(fark, cv2.COLOR_BGR2GRAY)  # görüntü gray tona çeviriliyor
        ret, fark = cv2.threshold(fark, 200, 255, cv2.THRESH_BINARY)  # binary tabana çevirilmesi

        fark1 = isaret_temp
        # fark1 = cv2.cvtColor(fark1, cv2.COLOR_BGR2GRAY)
        # ret, fark1 = cv2.threshold(fark1,200,255,cv2.THRESH_BINARY)

        px = fark  # fark px matrisi px değişkenine iletiliyor
        px1 = fark1
        say_fark = 0  # siyah pixel saydırmak için sayaç tutuluyor
        say_fark1 = 0

        for k in range(0, 50):
            for t in range(0, 60):
                if px[k][t] == 0:
                    say_fark += 1  # siyah pixeller sayılıyor
        for k in range(0, 40):
            for t in range(0, 40):
                if px1[k][t] == 0:
                    say_fark1 += 1  # siyah pixeller sayılıyor
        siyah_fark = abs(say_fark1 - say_fark)

        if siyah_fark > 350:
            print(int(i / 2) + 1, ". doğru yanlış sorusunun ", int(j + 1), ". şıkkı-->farkı", siyah_fark)
            cv2.rectangle(thresh2, (koordinat_dy[i][0], koordinat_dy[i][1]), ((koordinat_dy[i][0]) + 244, (koordinat_dy[i][1]) + 60), (0, 255, 0), 5)
        else:
            cv2.rectangle(thresh2, (koordinat_dy[i][0], koordinat_dy[i][1]), ((koordinat_dy[i][0]) + 244, (koordinat_dy[i][1]) + 60), (0, 0, 255), 5)
        i += 1
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # -------------------------şıklı soruların okunması için yapılan işlemler--------------------------------------------------------------------------------------------
    for i in range(0, len(temps)):  # şıkların koordinatları bulunuyor
        res = cv2.matchTemplate(img_gray, temps[i], cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        pt = []
        for pt in zip(*loc[::-1]):
            if len(pos_sk) == 0:
                pos_sk.append(pt)
            else:
                a = pt[0] - pos_sk[len(pos_sk) - 1][0]  # şıkların birbirlerine uzaklıkları hesaplanıyor
                b = pt[1] - pos_sk[len(pos_sk) - 1][1]
                a = a * a
                b = b * b
                m = math.sqrt(a + b)
                if m < 10:
                    continue
                else:
                    pos_sk.append(pt)

    kernel = np.ones((3, 3), np.uint8)  # dilasyon için kernel matris belirleniyor

    i = 0
    sk_say = len(pos_sk)
    soru_say = (sk_say) // 4
    print("sk_say", sk_say)
    print("soru_say", soru_say)

    while i < soru_say:
        j = i
        while j < sk_say:
            koordinat_sk.append(pos_sk[j])  # şıklar A1B1C2D2 şeklinde sıralanıyor
            j += (soru_say)
        i += 1

    for i in range(0, len(koordinat_sk)):
        sk.append(thresh2[(koordinat_sk[i][1]):(koordinat_sk[i][1]) + 70, (koordinat_sk[i][0]):(koordinat_sk[i][0]) + 100])
        sk1.append(thresh3[(koordinat_sk[i][1]):(koordinat_sk[i][1]) + 70, (koordinat_sk[i][0]):(koordinat_sk[i][0]) + 100])

    print("KİTAPÇIK NO:", s)

    i = 0
    #dogru_sk.append(str(s))
    while i < sk_say:
        j = i % 4
        fark = sk[i]

        fark = cv2.cvtColor(fark, cv2.COLOR_BGR2GRAY)  # görüntü gray tona çeviriliyor
        ret, fark = cv2.threshold(fark, 200, 255, cv2.THRESH_BINARY)

        fark1 = temps1[j]
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
            for t in range(0, 100):
                if px[k][t] == 0:
                    say_fark += 1  # siyah pixeller sayılıyor

        for k in range(0, 70):
            for t in range(0, 100):
                if px1[k][t] == 0:
                    say_fark1 += 1  # siyah pixeller sayılıyor

        siyah_fark = abs(say_fark1 - say_fark)

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
                cv2.rectangle(thresh2, (koordinat_sk[i][0], koordinat_sk[i][1]), ((koordinat_sk[i][0]) + 100, (koordinat_sk[i][1]) + 70), (0, 255, 0), 5)
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
                    cv2.rectangle(thresh2, (koordinat_sk[i - 1][0], koordinat_sk[i - 1][1]), ((koordinat_sk[i - 1][0]) + 100, (koordinat_sk[i - 1][1]) + 70), (0, 0, 255), 5)
                    cv2.rectangle(thresh2, (koordinat_sk[i][0], koordinat_sk[i][1]), ((koordinat_sk[i][0]) + 100, (koordinat_sk[i][1]) + 70), (0, 255, 0), 5)
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

                    cv2.rectangle(thresh2, (koordinat_sk[i - 1][0], koordinat_sk[i - 1][1]), ((koordinat_sk[i - 1][0]) + 100, (koordinat_sk[i - 1][1]) + 70), (0, 255, 0), 5)
                    cv2.rectangle(thresh2, (koordinat_sk[i][0], koordinat_sk[i][1]), ((koordinat_sk[i][0]) + 100, (koordinat_sk[i][1]) + 70), (0, 0, 255), 5)

        else:
            cv2.rectangle(thresh2, (koordinat_sk[i][0], koordinat_sk[i][1]), ((koordinat_sk[i][0]) + 100, (koordinat_sk[i][1]) + 70), (0, 0, 255), 5)
        i += 1

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("-------------------------------------------------------")
    print(birden_fazla)
    print("-------------------------------------------------------")
    cv2.imwrite('C:\\Users\\NovaPM\\Desktop\\' + str(s) + '_dogru_cevap.png', thresh2)
    return dogru_sk

def cevap_oku_fark(image1, temp1, image2, temp2):
    gelen = [image1, temp1, image2, temp2]

    kernel = np.ones((3, 3), np.uint8)  # kalıntılara uygulanacak dilasyon için 3x3 boyutunda birim matris oluşturuldu
    temp_say_siyah = 0
    x = 0
    secim = []  # şıkları karşılaştırmak için seçim dizisi oluşturuldu
    while x < len(gelen):

        fark = cv2.addWeighted(gelen[x], 0.7, gelen[x + 1], 0.3, 0)  # işaretli şık işaretlenmemiş şıkkın üzerinde saydam bir şekilde yerleştiriliyor

        fark[np.where((fark <= [20, 20, 20]).all(axis=2))] = [255, 255, 255]  # siyah olan pikseller siliniyor

        fark = cv2.dilate(fark, kernel, iterations=1)  # kalıntılara dilasyon uygulanıyor

        fark = cv2.cvtColor(fark, cv2.COLOR_BGR2GRAY)  # çıkan fark görüntüsü yani işaret gri tona çeviriliyor
        ret, fark = cv2.threshold(fark, 200, 255,
                                  cv2.THRESH_BINARY)  # saydam görüntü siyah tona çevirilmesi için binary tabana çeviriliyor

        px = fark  # fark matrisi px değişkenine atanıyor
        say_siyah = 0  # siyah pixel saydırmak için sayaç tutuluyor
        for k in range(0, 70):
            for t in range(0, 100):
                if px[k][t] == 0:
                    say_siyah += 1  # siyah pixeller sayılıyor
        secim.append(say_siyah)  # hesaplanan siyah pikseller seçim dizisine atanıyor
        x = x + 2
    print("secim dizisi", secim)
    fark = secim[0] - secim[1]  # gelen iki şıkkın işaret piksel farkı bulunuyor
    if fark > 250:  # belirlenen eşiğin üstünde olan doğru şık olarak return ediliyor
        return 0
    else:
        return 1