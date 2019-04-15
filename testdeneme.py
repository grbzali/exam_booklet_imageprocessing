import cv2
import numpy as np

koordinat_sk = [(154, 358), (152, 443), (152, 531), (152, 619), (153, 823), (152, 908), (152, 995), (152, 1083), (153, 1288), (152, 1372), (152, 1459), (152, 1548), (154, 1752), (152, 1836), (152, 1924), (152, 2012), (154, 2284), (152, 2368), (152, 2456), (152, 2544), (154, 2748), (152, 2834), (152, 2920), (152, 3009)]
coords = []

i = 1

print(len(koordinat_sk))

for i in range(len(koordinat_sk)):
    if i % 2 == 0:

        coords[i][0] = koordinat_sk[i][0]
        coords[i][1] = koordinat_sk[i][1]
        coords[i+1][0] = koordinat_sk[i][0] + 100
        coords[i+1][1] = koordinat_sk[i][1] + 70

    else:
        print(coords)
