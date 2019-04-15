import cv2

temp_sol_ust = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\sol_ust2.png', 0)
temp_sag_ust = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\sag_ust2.png', 0)
temp_sol_alt = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\sol_alt2.png', 0)
temp_sag_alt = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\sag_alt2.png', 0)
w, h = temp_sol_ust.shape[::-1]

def get_positions(image):
    noise_image = image  # gelen görüntü değişkene atandı

    koordinatlar = []  # koordinatların tutulması için gerekli dizi tanımlandı
    image_gray = cv2.cvtColor(noise_image, cv2.COLOR_BGR2GRAY)  # gelen görüntü gri tona çevrildi
    temps = [temp_sol_ust, temp_sag_ust, temp_sol_alt, temp_sag_alt]  # aranacak referanslar biz dizide tutuldu

    for x in temps:
        res = cv2.matchTemplate(image_gray, x,
                                cv2.TM_CCOEFF_NORMED)  # görüntü üzerinde template eşleştirmesi ile referanslar bulundu
        threshold = 0.9  # eşleştirmede eşleşen görüntüler için bir eşik değeri belirlendi
        loc = np.where(res >= threshold)  # eşik değerinden yüksek olan lokasyonlar belirlendi
        pt = []

        for pt in zip(*loc[::-1]):  # gelen lokasyonların piksel cinsinden koordinatları belirlendi
            cv2.rectangle(noise_image, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)

        koordinat = []

        if len(pt) != 0:  # pozisyon bilgileri koordinat dizisinde tutuluyor
            koordinat.append(pt[0])
            koordinat.append(pt[1])
        else:  # pozisyon bilgilerinin gelmemesi durumunda o değer sıfır olarak atanıyor
            koordinat.append(0)
            koordinat.append(0)

        koordinatlar.append(koordinat)

    bulunamayanlar = []

    for i in range(4):  #hangi koordinatın değerinin olmadığı saptanıyor
        if (koordinatlar[i][0] == 0) & (koordinatlar[i][1] == 0):
            bulunamayanlar.append(i)

    if len(bulunamayanlar) == 0:  # pozisyon bilgileri tam geliyorsa eğer geri döndürülüyor
        return koordinatlar

    elif len(bulunamayanlar) == 1:  # 3 tane referansın bulunması durumunda bulunamayan koordinatın değeri giriliyor.
        if (bulunamayanlar[0] == 0):
            koordinatlar[0][0] = koordinatlar[2][0]
            koordinatlar[0][1] = koordinatlar[1][1]

        elif (bulunamayanlar[0] == 1):
            koordinatlar[1][0] = koordinatlar[3][0]
            koordinatlar[1][1] = koordinatlar[0][1]

        elif (bulunamayanlar[0] == 2):
            koordinatlar[2][0] = koordinatlar[0][0]
            koordinatlar[2][1] = koordinatlar[3][1]

        else:
            koordinatlar[3][0] = koordinatlar[1][0]
            koordinatlar[3][1] = koordinatlar[2][1]

    elif len(
            bulunamayanlar) > 1:  # 1' den fazla bulunamayan referans olması durumunda kağıt okunamadı bilgisi veriliyor.
        print("Kağıt okunamadı!")
    print(koordinatlar)
    return koordinatlar
