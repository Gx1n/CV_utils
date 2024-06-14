import cv2
import os
import numpy as np
import time
import matplotlib.pyplot as plt

def pyramid_match(image, template):
    # 将图像和模板转换为灰度
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # 获取模板的尺寸
    tH, tW = template_gray.shape[:2]
    scale_list = [2 ** i for i in range(3)]
    crop = np.zeros_like(template)
    # 遍历图像金字塔
    #for floor, scale in enumerate(scale_list):
    # 根据比例因子缩放图像并保持纵横比
    scale = 4
    resized = cv2.resize(image_gray, (int(image_gray.shape[1] // scale), int(image_gray.shape[0] // scale)))
    tresized = cv2.resize(template_gray, (int(template_gray.shape[1] // scale), int(template_gray.shape[0] // scale)))

    #if floor + 1 == len(scale_list):
    result = cv2.matchTemplate(resized, tresized, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    top_left_restore = [x * scale for x in top_left] # 坐标还原
    crop = image_gray[top_left_restore[1]:top_left_restore[1] + tH,
           top_left_restore[0]:top_left_restore[0] + tW]
    # fig = plt.figure(figsize=(8, 10))
    # ax = fig.add_subplot(111)
    # ax.imshow(crop, cmap='gray')
    # plt.show()
    # plt.close(fig)
    return crop

if __name__ == '__main__':
    img_dir = "/home/tsdl/SBMV/数据/VG2S/VG2S_OK/up"

    # img = cv2.imread(r"res_img/VG2S/2.png")
    template = cv2.imread(r'/home/tsdl/SBMV/package/snd_sbmv_xray/std/VG2S_up_template.png')
    # crop = pyramid_match(img, template)
    # cv2.imwrite(os.path.join("/res_img/VG2S/2.png"), crop)

    for file in os.listdir(img_dir):
        img = cv2.imread(os.path.join(img_dir, file))
        start = time.time()
        crop = pyramid_match(img, template)
        end = time.time()
        print(f"消耗时间{end - start}")
        # fig = plt.figure(figsize=(8, 10))
        # ax = fig.add_subplot(111)
        # ax.imshow(crop, cmap='gray')
        # plt.show()
        # plt.close(fig)

        cv2.imwrite(os.path.join("/home/tsdl/SBMV/数据/VG2S/VG2S_OK/up_tpl", file), crop)