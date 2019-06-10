import cv2
from glob import glob
import pyzbar.pyzbar as pyzbar
import numpy as np
from pdf2image import convert_from_path
import skew_positions
import rotate_img
import skew_image
import json
from main_img import main
import dbactions
import time

temp_sol_ust = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\sol_ust2.png', 0)
temp_sag_ust = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\sag_ust2.png', 0)
temp_sol_alt = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\sol_alt2.png', 0)
temp_sag_alt = cv2.imread('C:\\Users\\NovaPM\\Desktop\\test_img\\sag_alt2.png', 0)
w, h = temp_sol_ust.shape[::-1]
temps = [temp_sol_ust, temp_sag_ust, temp_sol_alt, temp_sag_alt]
print(w, h)

A_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\temps\\A.png')
ret, A_temp1 = cv2.threshold(A_temp1, 200, 255, cv2.THRESH_BINARY)
B_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\temps\\B.png')
ret, B_temp1 = cv2.threshold(B_temp1, 200, 255, cv2.THRESH_BINARY)
C_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\temps\\C.png')
ret, C_temp1 = cv2.threshold(C_temp1, 200, 255, cv2.THRESH_BINARY)
D_temp1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\temps\\D.png')
ret, D_temp1 = cv2.threshold(D_temp1, 200, 255, cv2.THRESH_BINARY)

temps1 = [A_temp1, B_temp1, C_temp1, D_temp1]
start_time = int(round(time.time() * 1000))

def decode(im):
    # Find barcodes and QR codes

    decodedObjects = pyzbar.decode(im)
    print("decode obje", decodedObjects)
    if decodedObjects == []:
        return [], ""
    # Print results
    else:
        for obj in decodedObjects:
            print('Type : ', obj.type)
            print('Data : ', obj.data, '\n')

        return decodedObjects, obj.data

def display(im, decodedObjects):
    # Loop over all decoded objects
    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        # Number of points in the convex hull
        n = len(hull)


        if hull[0][1] > 2500:
            return True
            for j in range(0, len(hull)):
                cv2.line(im, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        else:
            for j in range(0, len(hull)):
                cv2.line(im, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
            return False

        # Draw the convext hull

    # Display results
    #im = cv2.resize(im, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_CUBIC)
    #cv2.imshow("Results", im);
    #cv2.waitKey(0);

filename = 'C:\\Users\\NovaPM\\Desktop\\denemes\\test_b_kit.PDF'

path = 'C:\\Users\\NovaPM\\Desktop\\denemes\\isare'

#pdf2image
#images = convert_from_path('C:\\Users\\NovaPM\\Desktop\\denemes\\test\\11UY0011-2 Ahşap Kalıpçı(Seviye 3) A1 A Grubu.PDF', dpi=300, output_folder=path, fmt='JPEG', output_file="sayfa")

kitapcik_id_temp = []
kitapcik_id = 0

jpg_say = len(glob("C:\\Users\\NovaPM\\Desktop\\denemes\\isaretli\\*.jpg"))  # klasördeki frame sayısı
print(" Dizinde", jpg_say, "Image bulunuyor.")

i = 1
j = 0
pos = 0
kitapcik_id_temp1 = []
cevap_sk = ''
sumdogru_sk = []
dogru_sk = []
temp_aday_id = []


#main loop


while i <= (jpg_say):

    print("i değeri", i)

    im = 0
    if i < 10:
        im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\denemes\\isaretli\\sayfa-0'+str(i)+'.jpg')
        #im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretsiz\\sayfa-0' + str(i) + '.jpg')
    else:
        im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\denemes\\isaretli\\sayfa-' + str(i) + '.jpg')
        #im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretsiz\\sayfa-' + str(i) + '.jpg')

#----barkod kontrol

    decodedObjects, data = decode(im)

    if decodedObjects == []:
        print("barkod bulunamadı")

        i += 1

        continue
    else:

        a = display(im, decodedObjects)

        barcode = data[2:]
        kitapcik_id = data[2:9]
        print(kitapcik_id)
        kitapcik_id_temp.append(kitapcik_id)

        # veritabanı pozisyon ve id sorguları
        connection = dbactions.dbconnect()

        positions, aday_id = dbactions.dbgetbarcode(connection, barcode)
        temp_aday_id.append(aday_id)

        y = json.loads(positions)

        if a == False:

            print("barkod bulunamadı")
            i += 1

            continue

        else:

    #----rotate
            e1 = cv2.getTickCount()

            rotated_image1 = rotate_img.rotate(im)

            e2 = cv2.getTickCount()
            t = (e2 - e1) / cv2.getTickFrequency()
            print("rotated image ", t*1000, "ms")
            #rotated_image2 = rotate_img.rotate(im1)

    #skew için köşe koordinatları alma
            e1 = cv2.getTickCount()

            coords_marked = skew_positions.get_positions(rotated_image1, temps, w, h)
            #coords_raw = skew_positions.get_positions(rotated_image2)

            e2 = cv2.getTickCount()
            t = (e2 - e1) / cv2.getTickFrequency()
            print("position image ", t*1000, "ms")

    #kesme işlemi

            e1 = cv2.getTickCount()

            images1 = skew_image.skew(coords_marked, rotated_image1, w, h)
            #images2 = skew_image.skew(coords_raw, rotated_image2)

            e2 = cv2.getTickCount()
            t = (e2 - e1) / cv2.getTickFrequency()
            print("skew image ", t * 1000, "ms")

            # temps = creat_temps.temps(images2, y, i)

            farktemp = len(dogru_sk)
            e1 = cv2.getTickCount()

            dogru_sk = main(images1, i, y, temps1)

            e2 = cv2.getTickCount()
            t = (e2 - e1) / cv2.getTickFrequency()
            print("main ", t * 1000, "ms")
            farktemp2 = len(dogru_sk)

            sayıfark = farktemp2-farktemp

    #okunan sayfaların kitapcık olarak toplanması

            if kitapcik_id_temp[j] != kitapcik_id_temp[j-1]:

                dogru_sk1 = dogru_sk[0:len(dogru_sk) - sayıfark]
                del dogru_sk[:len(dogru_sk)-sayıfark]

                dogru_sk1 = dogru_sk1[::-1]

                for k in range(len(dogru_sk1)-1, -1, -1):

                     cevap_sk += dogru_sk1[k]

                print("Kitapçık cevapları için")
                print(dogru_sk1, " ------- ", cevap_sk)

                dbactions.dbinsert(connection, temp_aday_id[len(temp_aday_id)-2], kitapcik_id_temp[j-1], cevap_sk)
                cevap_sk = ''

            elif i == jpg_say:
                dogru_sk = dogru_sk[::-1]
                cevap_sk = ''
                for k in range(len(dogru_sk)-1, -1, -1):

                    cevap_sk += dogru_sk[k]

                print("Son kitapçık cevapları için")
                print(dogru_sk, "----------", cevap_sk)
                dbactions.dbinsert(connection, aday_id, kitapcik_id, cevap_sk)

            else:
                print('Kitapçık tamamlanmadı.')
            j += 1
            i += 1