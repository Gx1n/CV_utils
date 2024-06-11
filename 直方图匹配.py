import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import os

def generate_horizontal_gradient(width=580, height=580):
    # 创建一个水平渐变的灰度图像
    gradient = np.tile(np.linspace(0, 255, width), (height, 1))
    cv2.imwrite('./res_img/horizontal.png', gradient)
    return gradient.astype(np.uint8)

def histogram_RGBmatch(source_image, reference_image):
    # 分离源图像和参考图像的三个通道
    source_channels = cv2.split(source_image)
    reference_channels = cv2.split(reference_image)

    matched_channels = []

    # 对每个通道分别进行直方图匹配
    for source_channel, reference_channel in zip(source_channels, reference_channels):
        # 计算两个图像的直方图
        source_hist, bins = np.histogram(source_channel.flatten(), 256, [0, 256])
        reference_hist, bins = np.histogram(reference_channel.flatten(), 256, [0, 256])

        # 计算累积分布函数(cdf)
        source_cdf = source_hist.cumsum()
        reference_cdf = reference_hist.cumsum()

        # 归一化累积分布函数到0-255之间
        source_cdf = (source_cdf / source_cdf[-1]) * 255
        reference_cdf = (reference_cdf / reference_cdf[-1]) * 255

        # 创建一个映射表，将源图的亮度值映射到参照图的亮度值
        histogram_map = np.zeros(256, dtype=np.uint8)
        for i in range(256):
            closest_value_index = np.abs(reference_cdf - source_cdf[i]).argmin()
            histogram_map[i] = closest_value_index

        # 应用映射表到源图像
        matched_channel = cv2.LUT(source_channel, histogram_map)
        matched_channels.append(matched_channel)

    # 合并处理后的三个通道
    matched_image = cv2.merge(matched_channels)

    return matched_image


def histogram_match(source_image, reference_image):
    # 计算两个图像的直方图
    source_hist, bins = np.histogram(source_image.flatten(), 256, [0, 256])
    reference_hist, bins = np.histogram(reference_image.flatten(), 256, [0, 256])

    # 计算累积分布函数(cdf)
    source_cdf = source_hist.cumsum()
    reference_cdf = reference_hist.cumsum()

    # 归一化累积分布函数到0-255之间
    source_cdf = (source_cdf / source_cdf[-1]) * 255
    reference_cdf = (reference_cdf / reference_cdf[-1]) * 255

    # 创建一个映射表，将源图的亮度值映射到参照图的亮度值
    histogram_map = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        closest_value_index = np.abs(reference_cdf - source_cdf[i]).argmin()
        histogram_map[i] = closest_value_index

    # 应用映射表到源图像
    matched_image = cv2.LUT(source_image, histogram_map)

    cv2.imwrite('./res_img/VG2S/img.png', source_image)
    cv2.imwrite('./res_img/VG2S/imgOut.png', matched_image)
    return matched_image


if __name__ == "__main__":
    # source_image = cv2.imread(r'/home/tsdl/SBMV/数据/VG2S/VG2S_OK/颜色对比/BC23#1_#0_2024022008543208.png')
    # reference_image = cv2.imread(r'/home/tsdl/SBMV/数据/VG2S/VG2S_OK/颜色对比/2.png')
    # start_time = time.time()
    # histogram_match(source_image, reference_image)
    # end_time = time.time()
    # print(end_time - start_time)

    dir_path = r"/home/tsdl/SBMV/数据/VG2S/VG2S_OK/up_tpl"
    reference_image = cv2.imread(r'/home/tsdl/SBMV/package/snd_sbmv_xray/std/VG2S_up_template.png')
    for file in os.listdir(dir_path):
        img = cv2.imread(os.path.join(dir_path, file))
        start_time = time.time()
        matched_image = histogram_match(img, reference_image)
        end_time = time.time()
        print(end_time - start_time)
        cv2.imwrite(os.path.join('/home/tsdl/SBMV/数据/VG2S/VG2S_OK/up_match', file), matched_image)