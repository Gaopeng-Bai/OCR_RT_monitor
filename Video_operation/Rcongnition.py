#!/usr/bin/env python
# encoding: utf-8
"""
@author: Gaopeng
@license: (C) Copyright 2016-2020, Node Supply Chain Manager Corporation Limited.
@contact: gaopengbai0121@gmail.com
@software: Pycharm
@file: Rcongnition.py
@time: 1/8/2020 11:39 AM
@desc:
"""
try:
    from PIL import Image, ImageFilter
except ImportError:
    import Image
import cv2
import pytesseract

threshold = 110
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    # noise filter, and convert to gray image
    im = Image.open(filename)
    im = im.convert('L')
    # # im = im.filter(ImageFilter.EDGE_ENHANCE)
    out = im.point(table, '1')
    # out.show()

    text = pytesseract.image_to_string(out)  # We'll use Pillow's Image class to open the image and pytesseract to
    # detect the string in the image
    return text


if __name__ == "__main__":
    print("test : " + ocr_core("../1.png"))
