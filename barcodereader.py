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

        # Draw the convext hull
        for j in range(0, n):
            cv2.line(im, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

    # Display results
    #im = cv2.resize(im, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_CUBIC)
    #cv2.imshow("Results", im);
    #cv2.waitKey(0);

filename = 'C:\\Users\\NovaPM\\Desktop\\denemes\\test_b_kit.PDF'

path = 'C:\\Users\\NovaPM\\Desktop\\denemes'

#images = convert_from_path('C:\\Users\\NovaPM\\Desktop\\denemes\\test_b_kit.PDF', dpi=300, output_folder=path, fmt='JPEG', output_file="sayfa") #pdf2image

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

while i <= (jpg_say):
    print("i değeri", i)
    finish_time = int(round(time.time() * 1000))
    print("imreadönce", (finish_time) - (start_time), "Ms")

    im = 0
    if i < 10:
        im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretli\\sayfa-0'+str(i)+'.jpg')
        #im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretsiz\\sayfa-0' + str(i) + '.jpg')
    else:
        im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretli\\sayfa-' + str(i) + '.jpg')
        #im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretsiz\\sayfa-' + str(i) + '.jpg')

    finish_time = int(round(time.time() * 1000))
    print("decodeönce", (finish_time) - (start_time), "Ms")

    decodedObjects, data = decode(im)
    finish_time = int(round(time.time() * 1000))
    print("decode sonra", (finish_time) - (start_time), "Ms")

    if decodedObjects == []:
        print("barkod bulunamadı")

        i += 1

        continue
    else:
        #display(im, decodedObjects)
        # print(data[0:-4])
        # print(data[9:-1])

        barcode = data[2:]
        kitapcik_id = data[2:9]
        print(kitapcik_id)
        kitapcik_id_temp.append(kitapcik_id)

        finish_time = int(round(time.time() * 1000))
        print("rotated_image önce", (finish_time) - (start_time), "Ms")

        rotated_image1 = rotate_img.rotate(im)
        finish_time = int(round(time.time() * 1000))
        print("ilk rotated_image sonra", (finish_time) - (start_time), "Ms")

        #rotated_image2 = rotate_img.rotate(im1)
        finish_time = int(round(time.time() * 1000))
        print("ikinci rotated_image sonra", (finish_time) - (start_time), "Ms")

        coords_marked = skew_positions.get_positions(rotated_image1)
        finish_time = int(round(time.time() * 1000))
        print("coords_image sonra", (finish_time) - (start_time), "Ms")

        #coords_raw = skew_positions.get_positions(rotated_image2)
        #finish_time = int(round(time.time() * 1000))
        #print("coords2_image sonra", (finish_time) - (start_time), "Ms")

        images1 = skew_image.skew(coords_marked, rotated_image1)
        finish_time = int(round(time.time() * 1000))
        print("1skew_imagesonra", (finish_time) - (start_time), "Ms")

        #images2 = skew_image.skew(coords_raw, rotated_image2)
        #finish_time = int(round(time.time() * 1000))
        #print("2.skew_imagesonra", (finish_time) - (start_time), "Ms")

        connection = dbactions.dbconnect()

        positions, aday_id = dbactions.dbgetbarcode(connection, barcode)

        temp_aday_id.append(aday_id)

        y = json.loads(positions)

        # temps = creat_temps.temps(images2, y, i)

        farktemp = len(dogru_sk)

        finish_time = int(round(time.time() * 1000))
        print("main öncesi", (finish_time) - (start_time), "Ms")

        dogru_sk = main(images1, i, y)
        finish_time = int(round(time.time() * 1000))
        print("main_sonrası", (finish_time) - (start_time), "Ms")

        farktemp2 = len(dogru_sk)

        sayıfark = farktemp2-farktemp

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
        finish_time = int(round(time.time() * 1000))
        print("imageson", (finish_time) - (start_time), "Ms")
        j += 1
        i += 1
