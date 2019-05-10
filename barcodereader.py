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

im = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretli\\sayfa-17.jpg')
im1 = cv2.imread('C:\\Users\\NovaPM\\Desktop\\Barkod_okuyucu\\isaretsiz\\sayfa-17.jpg')

rotated_image1 = rotate_img.rotate(im)
rotated_image2 = rotate_img.rotate(im1)

coords_marked = skew_positions.get_positions(rotated_image1)
coords_raw = skew_positions.get_positions(rotated_image2)

images1 = skew_image.skew(coords_marked, rotated_image1)
images2 = skew_image.skew(coords_raw, rotated_image2)

#dbcoords

coords = '{"sorular":[{"a":{"center":{"first":{"x":"152","y":"358"},"second":{"x":"252","y":"428"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"b":{"center":{"first":{"x":"152","y":"443"},"second":{"x":"252","y":"513"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"c":{"center":{"first":{"x":"152","y":"531"},"second":{"x":"252","y":"601"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"d":{"center":{"first":{"x":"152","y":"619"},"second":{"x":"252","y":"689"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}}},{"a":{"center":{"first":{"x":"152","y":"823"},"second":{"x":"252","y":"893"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"b":{"center":{"first":{"x":"152","y":"908"},"second":{"x":"252","y":"978"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"c":{"center":{"first":{"x":"152","y":"995"},"second":{"x":"252","y":"1065"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"d":{"center":{"first":{"x":"152","y":"1083"},"second":{"x":"252","y":"1153"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}}},{"a":{"center":{"first":{"x":"152","y":"1355"},"second":{"x":"252","y":"1425"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"b":{"center":{"first":{"x":"152","y":"1440"},"second":{"x":"252","y":"1510"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"c":{"center":{"first":{"x":"152","y":"1527"},"second":{"x":"252","y":"1597"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"d":{"center":{"first":{"x":"152","y":"1615"},"second":{"x":"252","y":"1685"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}}},{"a":{"center":{"first":{"x":"152","y":"1887"},"second":{"x":"252","y":"1957"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"b":{"center":{"first":{"x":"152","y":"1972"},"second":{"x":"252","y":"2042"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"c":{"center":{"first":{"x":"152","y":"2059"},"second":{"x":"252","y":"2129"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"d":{"center":{"first":{"x":"152","y":"2147"},"second":{"x":"252","y":"2217"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}}},{"a":{"center":{"first":{"x":"152","y":"2419"},"second":{"x":"252","y":"2489"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"b":{"center":{"first":{"x":"152","y":"2504"},"second":{"x":"252","y":"2574"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"c":{"center":{"first":{"x":"152","y":"2591"},"second":{"x":"252","y":"2661"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}},"d":{"center":{"first":{"x":"152","y":"2679"},"second":{"x":"252","y":"2749"}},"left":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}},"right":{"first":{"x":"100","y":"200"},"second":{"x":"170","y":"270"}}}}]}'
y = json.loads(coords)

#temps = creat_temps.temps(images2, y, i)

dogru_sk = main(images1, images2, i, y)

i += 1

print(dogru_sk)
