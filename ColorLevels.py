# -*- coding: utf-8 -*-
# @Time    : 2021-02-24 16:45
# @Author  : AlanWang4523
# @FileName: ps_levels.py

import os
import sys
import cv2
import numpy as np


class Levels:
    """
    @Author  : AlanWang4523
    色阶调整类，根据输入参数调整图片色阶，并输出处理后的图片
    """

    def __init__(self):
        self.channel = 0
        self.input_shadows = 0
        self.input_highlights = 255
        self.midtones = 1.0
        self.output_shadows = 0
        self.output_highlights = 255

    def adjust_image(self, img):
        print("Levels Params:")
        print("          channel:", self.channel)
        print("    input_shadows:", self.input_shadows)
        print(" input_highlights:", self.input_highlights)
        print("         midtones:", self.midtones)
        print("   output_shadows:", self.output_shadows)
        print("output_highlights:", self.output_highlights)
        print("")

        img = img.astype(np.float)

        # 输入色阶映射
        img = 255 * ((img - self.input_shadows) / (self.input_highlights - self.input_shadows))
        img[img < 0] = 0
        img[img > 255] = 255

        # 中间调处理
        img = 255 * np.power(img / 255.0, 1.0 / self.midtones)

        # 输出色阶映射
        img = (img / 255) * (self.output_highlights - self.output_shadows) + self.output_shadows
        img[img < 0] = 0
        img[img > 255] = 255

        img = img.astype(np.uint8)
        return img


# def level_adjust_and_save_img(origin_image):
#     levels.input_shadows = 40
#     levels.input_highlights = 240
#     levels.midtones = 0.60
#     levels.output_shadows = 30
#     levels.output_highlights = 220
#
#     image = levels.adjust_image(origin_image)
#
#     cv2.imwrite('py_test_out.png', image)


def level_adjust(path):
    """
    色阶调整
    """
    origin_image = cv2.imread(path)

    levels = Levels()

    def update_input_shadows(x):
        if (x < levels.input_highlights):
            levels.input_shadows = x

    def update_input_highlights(x):
        if (x > levels.input_shadows):
            levels.input_highlights = x

    def update_midtones(x):
        # 由于 midtones 的调整范围是 [9.99, 0.01]，Python 滑杆无法自定义显示小数，因此将滑杆的 [0, 100] 映射到 [9.99, 0.01]
        midtones = 1.0
        if (x < 50):
            midtones = 1 + 9 * ((50.0 - x) / 50.0)
        elif (x > 50):
            midtones = 1 - (x - 50) / 50.0

        levels.midtones = np.clip(midtones, 0.01, 9.99)
        # levels.midtones = 0.6 # 直接测试某个参数值

    def update_output_shadows(x):
        if (x < levels.output_highlights):
            levels.output_shadows = x

    def update_output_highlights(x):
        if (x > levels.output_shadows):
            levels.output_highlights = x

    # 创建图片显示窗口
    title = "Levels"
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title, 800, 600)
    cv2.moveWindow(title, 0, 0)

    # 创建色阶操作窗口
    option_title = "Option"
    cv2.namedWindow(option_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(option_title, 400, 200)
    cv2.moveWindow(option_title, 800, 0)

    cv2.createTrackbar('    input_shadows', option_title, levels.input_shadows, 255, update_input_shadows)
    cv2.createTrackbar(' input_highlights', option_title, levels.input_highlights, 255, update_input_highlights)
    cv2.createTrackbar('         midtones', option_title, 50, 100, update_midtones)
    cv2.createTrackbar('   output_shadows', option_title, levels.output_shadows, 255, update_output_shadows)
    cv2.createTrackbar('output_highlights', option_title, levels.output_highlights, 255, update_output_highlights)

    while True:
        image = levels.adjust_image(origin_image)
        cv2.imshow(title, image)
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    '''
    	Author: AlanWang4523
        运行环境：Python 3
        执行：python3 ps_levels.py <图片路径>
        如：python3 ps_levels.py test.jpg
    '''
    img_path = "/home/tsdl/SBMV/package/snd_sbmv_xray/std/VG2S_up_template.png"
    #/home/tsdl/SBMV/package/snd_sbmv_xray/std/BC23_template.png
    #/home/tsdl/AVXP/SE&BC23图片/SE1_0221/OK/down/SE1#1_9124642050#0_2024022113231101.png
    print("img_path Params:", img_path)
    level_adjust(img_path)
