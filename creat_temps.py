import cv2

def temps(image, coords, i):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh2 = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

    sorular = coords["sorular"]
    sk_temp = []

    for sklar in coords["sorular"][0]:
        sk_temp.append(
            thresh2[int((sorular[0][sklar]["center"]["first"]["y"])):int((sorular[0][sklar]["center"]["second"]["y"])),
            int((sorular[0][sklar]["center"]["first"]["x"])) - 50:int((sorular[0][sklar]["center"]["second"]["x"]))])

    cv2.imwrite('C:\\Users\\NovaPM\\Desktop\\temps\\A.png', sk_temp[0])
    cv2.imwrite('C:\\Users\\NovaPM\\Desktop\\temps\\B.png', sk_temp[1])
    cv2.imwrite('C:\\Users\\NovaPM\\Desktop\\temps\\C.png', sk_temp[2])
    cv2.imwrite('C:\\Users\\NovaPM\\Desktop\\temps\\D.png', sk_temp[3])

