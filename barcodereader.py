import cv2
from glob import glob
import pyzbar.pyzbar as pyzbar
import numpy as np
from pdf2image import convert_from_path
import skew_positions
import rotate_img
import skew_image
import cevap_oku

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

kitapcik_id_temp = 0
jpg_say = len(glob("C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretli\\*.jpg"))  # klasördeki frame sayısının alınması
print(jpg_say)
i = 1

while i <= (jpg_say):
    print("i değeri", i)
    if i < 10:
        im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretli\\sayfa-0' + str(i) + '.jpg')
        im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretsiz\\sayfa-0' + str(i) + '.jpg')
    else:
        im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretli\\sayfa-' + str(i) + '.jpg')
        im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretsiz\\sayfa-' + str(i) + '.jpg')
    decodedObjects, data = decode(im)

    if decodedObjects == []:
        print("barkod bulunamadı")
        i += 1
        continue
    else:
        display(im, decodedObjects)
        # print(data[0:-4])
        # print(data[9:-1])
        kitapcik_id = data[:9]

    i += 1
    rotated_image1 = rotate_img.rotate(im)
    rotated_image2 = rotate_img.rotate(im1)

    coords_marked = skew_positions.get_positions(rotated_image1)
    coords_raw = skew_positions.get_positions(rotated_image2)

    images1 = skew_image.skew(coords_marked, rotated_image1)
    images2 = skew_image.skew(coords_raw, rotated_image2)

    #dbcoords


    dogru_sk = cevap_oku.cevap_oku(images1, images2, i, coords)

    print(dogru_sk)
