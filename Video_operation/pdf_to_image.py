#!/usr/bin/env python
# encoding: utf-8
"""
@author: Gaopeng
@license: (C) Copyright 2016-2020, Node Supply Chain Manager Corporation Limited.
@contact: gaopengbai0121@gmail.com
@software: Pycharm
@file: pdf_to_image.py
@time: 1/14/2020 3:29 PM
@desc: Convert pdf file to image.
"""
# -*- coding: utf-8 -*-
import io

from wand.image import Image
from wand.color import Color
from PyPDF2 import PdfFileReader, PdfFileWriter
import os

memo = {}


def delete_file(keyword, root):
    filelist = []
    for root, dirs, files in os.walk(root):
        for name in files:
            filelist.append(os.path.join(root, name))
    for i in filelist:
        if os.path.isfile(i):
            if keyword in os.path.split(i)[1]:
                os.remove(i)


def getPdfReader(filename):
    reader = memo.get(filename, None)
    if reader is None:
        reader = PdfFileReader(filename, strict=False)
        memo[filename] = reader
    return reader


class pdf_to_image:

    def run_convert(self, filename, page, res=120):
        # idx = page + 1
        pdfile = getPdfReader(filename)
        pageObj = pdfile.getPage(page)
        dst_pdf = PdfFileWriter()
        dst_pdf.addPage(pageObj)

        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)

        img = Image(file=pdf_bytes, resolution=res)
        img.format = 'png'
        img.compression_quality = 100
        img.background_color = Color("white")
        filename = filename.split("/")[-1]
        self.img_path = '%s%s.png' % (filename[:filename.rindex('.')], "temp")
        delete_file("temp", root='.')
        img.save(filename=self.img_path)
        img.destroy()
