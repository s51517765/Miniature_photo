# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np


def main(file):
    filter_size = 4  # ぼかしの強さ
    image_input = np.array(Image.open(file), 'f')
    print("image shape = ", image_input.shape)
    # print(image_input[10,10])  # 指定した座標の画素値（R, G, B） / 原点は左上
    size_x = image_input.shape[0]  # 入力画像のサイズ
    size_y = image_input.shape[1]
    redion_x = size_x / 2  # ぼかし範囲 縦
    redion_y = size_y / 2.3  # ぼかし範囲 横

    image_output1 = np.zeros((size_x, size_y, 3))  # 中間出力
    image_output2 = np.zeros((size_x, size_y, 3))  # 最終出力
    for x in range(size_x):
        for y in range(size_y):
            for RGB in range(3):
                hankei = ((x - size_x / 2) / redion_x) ** 2 + ((y - size_y / 2) / redion_y) ** 2
                if filter_region(x, y, size_x, size_y, filter_size, hankei) == True:  # 外側がフィルター範囲
                    filterOutput = 0
                    for i in range(filter_size):
                        for j in range(filter_size):
                            filterOutput += image_input[x + i - int(filter_size / 2), y + j - int(filter_size / 2), RGB]
                    image_output1[x, y, RGB] = filterOutput / filter_size ** 2
                else:
                    image_output1[x, y, RGB] = image_input[x, y, RGB]
                image_output2[x, y, RGB] = tone_function(image_output1[x, y, RGB], x, y, RGB)  # 彩度が高いところ

    pil_img = Image.fromarray(np.uint8(image_output2))  # https://nixeneko.hatenablog.com/entry/2017/09/01/000000
    outputName = file[:len(file) - 4] + "_save.png"
    pil_img.save(outputName)


def tone_function(value, x, y, RGB):  # 彩度が高いところをより高く
    lowerLimit = 40
    outputValue = (value - lowerLimit) * 1.4 + lowerLimit
    if outputValue > 255:
        return 255
    elif value > lowerLimit:
        return outputValue
    else:
        value


def filter_region(x, y, size_x, size_y, filter_size, hankei):
    if x > filter_size / 2 and y > filter_size / 2 and x < size_x - filter_size / 2 and y < size_y - filter_size / 2 and hankei > 1:
        return True
    else:
        return False


if __name__ == '__main__':
    main("tokyu.jpg")
