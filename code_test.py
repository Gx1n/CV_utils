"""zxing"""
# import os
# import time
# import zxing
# from PIL import Image
#
# reader = zxing.BarCodeReader()
# code_path = "/home/tsdl/PycharmProjects/pythonProject1/code/ningde"
# for file in os.listdir(code_path):
#     start = time.time()
#     img_path = os.path.join(code_path, file)
#     if os.path.isfile(img_path):
#         img = Image.open(img_path)
#         results = reader.decode(img)
#         end = time.time()
#         print(results, f"\nTime cost: {end - start}s")

"""zxing-cpp"""
import cv2, zxingcpp, os, time
code_path = "/home/tsdl/PycharmProjects/pythonProject1/code"
for file in os.listdir(code_path):
    img_path = os.path.join(code_path, file)
    if os.path.isfile(img_path):
        gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        start = time.time()
        results = zxingcpp.read_barcodes(gray)
        for result in results:
            print('Found barcode:'
                  f'\n Text:    "{result.text}"'
                  f'\n Format:   {result.format}'
                  f'\n Content:  {result.content_type}'
                  f'\n Position: {result.position}')
        end = time.time()
        print(f"{file}\nTime cost: {end - start}s\n\n")

"""pylibdmtx"""
# import os
# import time
# import cv2
# from pylibdmtx import pylibdmtx
#
# code_path = "/home/tsdl/PycharmProjects/pythonProject1/code/ningde"
# # gray = cv2.imread("/home/tsdl/PycharmProjects/pythonProject1/code/ningde.jpg", cv2.IMREAD_GRAYSCALE)
# # results = pylibdmtx.decode(gray)
#
# # print(results, f"\nTime cost: {end - start}s")
# for file in os.listdir(code_path):
#     img_path = os.path.join(code_path, file)
#     if os.path.isfile(img_path):
#         gray = cv2.imread(os.path.join(code_path, file), cv2.IMREAD_GRAYSCALE)
#         start = time.time()
#         results = pylibdmtx.decode(gray)
#         end = time.time()
#         print(results, f"\n{file}\nTime cost: {end - start}s")

"""pyboof"""
# import numpy as np
# import pyboof as pb
#
# # 读取图像
# img = pb.load_single_band("/home/tsdl/PycharmProjects/pythonProject1/code/ningde/ningde1.png", np.uint8)
#
# # 创建解码器
# detector = pb.FactoryFiducial(np.uint8).qrcode()
#
# # 检测并解码
# detector.detect(img)
#
# # 展示解码结果
# print("检测到 {} 个QR码".format(len(detector.detections)))
# for qr in detector.detections:
#     print("Message: " + qr.message)
#     print("     at: " + str(qr.bounds))

