import cv2
from glob import glob
import pyzbar.pyzbar as pyzbar
import numpy as np
from pdf2image import convert_from_path
import skew_positions
import rotate_img
import skew_image
import creat_temps
import json
from main_img import main
import dbactions

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
    im = cv2.resize(im, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_CUBIC)
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
kitapcik_id_temp1 = []
cevap_sk = ''
sumdogru_sk = []
dogru_sk = []
while i <= (jpg_say):
    print("i değeri", i)

    im = 0
    if i < 10:
        im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\denemes\\isaretli\\sayfa-0' + str(i) + '.jpg')
        im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\denemes\\isaretsiz\\sayfa-0' + str(i) + '.jpg')
    else:
        im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\denemes\\isaretli\\sayfa-' + str(i) + '.jpg')
        im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\denemes\\isaretsiz\\sayfa-' + str(i) + '.jpg')

    decodedObjects, data = decode(im)

    if decodedObjects == []:
        print("barkod bulunamadı")

        i += 1

        continue
    else:
        display(im, decodedObjects)
        # print(data[0:-4])
         # print(data[9:-1])

        page_id = data[2:]
        kitapcik_id = data[2:9]

        kitapcik_id_temp.append(kitapcik_id)

        rotated_image1 = rotate_img.rotate(im)
        rotated_image2 = rotate_img.rotate(im1)

        coords_marked = skew_positions.get_positions(rotated_image1)
        coords_raw = skew_positions.get_positions(rotated_image2)

        images1 = skew_image.skew(coords_marked, rotated_image1)
        images2 = skew_image.skew(coords_raw, rotated_image2)

        connection = dbactions.dbconnect()

        positions, aday_id = dbactions.dbgetbarcode(connection, page_id)

        y = json.loads(positions)

        # temps = creat_temps.temps(images2, y, i)

        farktemp = len(dogru_sk)

        dogru_sk = main(images1, images2, i, y)

        farktemp2 = len(dogru_sk)

        sayıfark = farktemp2-farktemp
        print(sayıfark)


        if kitapcik_id_temp[j] != kitapcik_id_temp[j-1]:

            dogru_sk1 = dogru_sk[0:len(dogru_sk) - sayıfark]
            del dogru_sk[:len(dogru_sk)-sayıfark]

            dogru_sk1 = dogru_sk1[::-1]



            for k in range(len(dogru_sk1)-1, -1, -1):

                 cevap_sk += dogru_sk1[k]

            print("Kitapçık cevapları için")
            dbactions.dbinsert(connection, 11, kitapcik_id_temp[j-1], cevap_sk)

        elif i == jpg_say:
            dogru_sk = dogru_sk[::-1]
            cevap_sk = ''
            for k in range(len(dogru_sk)-1, -1, -1):


                cevap_sk += dogru_sk[k]

            print("Son kitapçık cevapları için")
            dbactions.dbinsert(connection, aday_id, kitapcik_id, cevap_sk)


        else:
            print('Kitapçık tamamlanmadı.')
        j += 1
        i += 1

