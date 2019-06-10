import cv2
import numpy as np

def rotate(image):
    image = image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # gelen görüntü gri tona çeviriliyor
    gray = cv2.bitwise_not(gray)

    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    coords = np.column_stack(np.where(thresh > 0))  # döndürülecek koordinat noktaları hesaplanıyor
    angle = cv2.minAreaRect(coords)[-1]  # kaç derece döndürüleceği hesaplanıyor

    if angle < -45:
        angle = -(90 + angle)

    else:
        angle = -angle

    (h, w) = image.shape[:2]  # görüntünün yüksekliği ve genişliği alınıyor
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)  # döndürülecek görüntünün merkezi ve döndürülecek açı tanımlanıyor

    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)  # Affine dönüşümü uygulanıyor görüntü gelen açıya uygun şekilde döndürülüyor

    cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
                # kaç derece döndürüldüğü frame'in sol üst köşesine yazılıyor
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # cv2.imshow('rotated', rotated)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return rotated



