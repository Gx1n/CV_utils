import cv2
import numpy as np


class HSV_Adjustment:
    def __init__(self):
        self.h_rate = 1.0
        self.s_rate = 1.0
        self.v_rate = 1.0

    def update_H(self, h):
        if h < 50:
            self.h_rate = h / 50.0
        else:
            self.h_rate = h / 50.0

    def update_S(self, s):
        if s < 50:
            self.s_rate = s / 50.0
        else:
            self.s_rate = s / 50.0

    def update_V(self, v):
        if v < 50:
            self.v_rate = v / 50.0
        else:
            self.v_rate = v / 50.0

    def adjust(self, h, s, v):
        h = h * self.h_rate
        h[h < 0] = 0
        h[h > 255] = 255

        s = s * self.s_rate
        s[s < 0] = 0
        s[s > 255] = 255

        v = v * self.v_rate
        v[v < 0] = 0
        v[v > 255] = 255

        img_modified = cv2.merge([h, s, v])
        img_hsv = img_modified.astype(np.uint8)
        img_modified = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        return img_hsv, img_modified

    def HSV_bar(self, img):
        option_title = "Option"
        cv2.namedWindow(option_title, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(option_title, 400, 200)

        cv2.createTrackbar('H_value', option_title, 50, 100, self.update_H)
        cv2.createTrackbar('S_value', option_title, 50, 100, self.update_S)
        cv2.createTrackbar('V_value', option_title, 50, 100, self.update_V)
        while 1:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            img_hsv, img_modified = self.adjust(h, s, v)
            img_modified = img_modified.astype(np.uint8)

            def getpos(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    print(img_hsv[y, x])

            cv2.namedWindow("img_hsv", 0)
            cv2.resizeWindow("img_hsv", 640, 1280)
            cv2.imshow('img_hsv', img_hsv)
            cv2.namedWindow("img_modified", 0)
            cv2.resizeWindow("img_modified", 640, 1280)
            cv2.imshow('img_modified', img_modified)
            cv2.setMouseCallback("img_hsv", getpos)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()



if __name__ == '__main__':
    img = cv2.imread('/home/tsdl/UnitTest/data/6/battery#4_3294#0_2023040411072211.png')
    tool = HSV_Adjustment()
    tool.HSV_bar(img)

