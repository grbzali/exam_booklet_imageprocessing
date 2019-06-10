import cv2
import numpy as np

def skew(coords, image, w, h):
    noise_image = image
    rows, cols, ch = noise_image.shape
    # w,h = image.shape[:2]                                                              #görüntünün yüksekliği ve genişliğini alır
    # print(w,h)
    sol_ust = coords[0]  # gelen koordinatların değerleri sırasıyla referanslara atanıyor
    sag_ust = coords[1]
    sol_alt = coords[2]
    sag_alt = coords[3]

    pts1 = np.float32([[sol_ust[0], sol_ust[1]], [sol_alt[0], sol_alt[1] + h], [sag_ust[0] + w, sag_ust[1]], [sag_alt[0] + w, sag_alt[1] + h]])  # belirlenen koordinatların değerleri float32 olarak pts1 referansına atanıyor
    pts2 = np.float32([[0, 0], [0, 3308], [2280, 0], [2280, 3308]])  # kırpma işlemi yapıldıktan sonra 2280-3308 boyutlarında bir çerçevenin boyutları pts2 ye atanıyor
    M = cv2.getPerspectiveTransform(pts1, pts2)
    width, hight = noise_image.shape[:2]
    dst = cv2.warpPerspective(noise_image, M, (2280, 3308))  # kırpma işlemi gerçekleştirilden sonra hedef görüntü dst değişkenine atanıyor

    # plt.subplot(121),plt.imshow(noise_image),plt.title('Input')
    # plt.subplot(122),plt.imshow(dst),plt.title('Output')
    # plt.show()
    #cv2.imwrite('C:\\Users\\NovaPM\\Desktop\\test_image\\orj_sskew.jpg',dst)
    return dst