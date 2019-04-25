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

images = convert_from_path('C:\\Users\\NovaPM\\Desktop\\denemes\\test_b_kit.PDF', dpi=300, output_folder=path, fmt='JPEG', output_file="sayfa") #pdf2image

kitapcik_id_temp = 0
jpg_say = len(glob("C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretli\\*.jpg"))  # klasördeki frame sayısı
print(jpg_say)

i = 1

#while i <= (jpg_say):
#    print("i değeri", i)
#    if i < 10:
#        im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretli\\sayfa-0' + str(i) + '.jpg')
#        im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretsiz\\sayfa-0' + str(i) + '.jpg')
#    else:
#        im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretli\\sayfa-' + str(i) + '.jpg')
#        im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretsiz\\sayfa-' + str(i) + '.jpg')
#    decodedObjects, data = decode(im)
#
#    if decodedObjects == []:
#        print("barkod bulunamadı")
#        i += 1
#        continue
#    else:
#        display(im, decodedObjects)
#        # print(data[0:-4])
#        # print(data[9:-1])
#        kitapcik_id = data[:9]

im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretli\\sayfa-21.jpg')
im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretsiz\\sayfa-21.jpg')

rotated_image1 = rotate_img.rotate(im)
rotated_image2 = rotate_img.rotate(im1)

coords_marked = skew_positions.get_positions(rotated_image1)
coords_raw = skew_positions.get_positions(rotated_image2)

images1 = skew_image.skew(coords_marked, rotated_image1)
images2 = skew_image.skew(coords_raw, rotated_image2)

#dbcoords

coords = '{"sorular":[{"a":{"center":{"first":{"x":"154","y":"290"},"second":{"x":"254","y":"360"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"b":{"center":{"first":{"x":"152","y":"376"},"second":{"x":"252","y":"446"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"c":{"center":{"first":{"x":"152","y":"463"},"second":{"x":"252","y":"533"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"d":{"center":{"first":{"x":"152","y":"551"},"second":{"x":"252","y":"621"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}}},{"a":{"center":{"first":{"x":"152","y":"756"},"second":{"x":"252","y":"826"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"b":{"center":{"first":{"x":"152","y":"840"},"second":{"x":"252","y":"910"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"c":{"center":{"first":{"x":"152","y":"927"},"second":{"x":"252","y":"997"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"d":{"center":{"first":{"x":"152","y":"1016"},"second":{"x":"252","y":"1086"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}}},{"a":{"center":{"first":{"x":"152","y":"1220"},"second":{"x":"252","y":"1290"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"b":{"center":{"first":{"x":"152","y":"1304"},"second":{"x":"252","y":"1374"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"c":{"center":{"first":{"x":"152","y":"1392"},"second":{"x":"252","y":"1462"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"d":{"center":{"first":{"x":"152","y":"1480"},"second":{"x":"252","y":"1550"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}}},{"a":{"center":{"first":{"x":"152","y":"1684"},"second":{"x":"252","y":"1754"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"b":{"center":{"first":{"x":"152","y":"1769"},"second":{"x":"252","y":"1839"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"c":{"center":{"first":{"x":"152","y":"1856"},"second":{"x":"252","y":"1926"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"d":{"center":{"first":{"x":"152","y":"1944"},"second":{"x":"252","y":"2014"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}}},{"a":{"center":{"first":{"x":"152","y":"2149"},"second":{"x":"252","y":"2219"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"b":{"center":{"first":{"x":"152","y":"2234"},"second":{"x":"252","y":"2304"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"c":{"center":{"first":{"x":"152","y":"2321"},"second":{"x":"252","y":"2391"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"d":{"center":{"first":{"x":"152","y":"2410"},"second":{"x":"252","y":"2480"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}}},{"a":{"center":{"first":{"x":"152","y":"2613"},"second":{"x":"252","y":"2683"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"b":{"center":{"first":{"x":"152","y":"2698"},"second":{"x":"252","y":"2768"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"c":{"center":{"first":{"x":"152","y":"2786"},"second":{"x":"252","y":"2856"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"d":{"center":{"first":{"x":"152","y":"2874"},"second":{"x":"252","y":"2944"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}}}]}'
y = json.loads(coords)

#temps = creat_temps.temps(images2, y, i)

dogru_sk = main(images1, images2, i, y)

i += 1

print(dogru_sk)
