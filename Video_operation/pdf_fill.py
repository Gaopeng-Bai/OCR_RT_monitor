#!/usr/bin/python3
# -*-coding:utf-8 -*-

# Reference:**********************************************
# @Time    : 9/30/2019 12:34 PM
# @Author  : Gaopeng.Bai
# @File    : add_pdf_fill.py
# @User    : baigaopeng
# @Software: PyCharm
# Reference:**********************************************

import io
import os
import time
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def fill_data_in_pdf(position: object, data_to_fill, original_pdf="haha.pdf",
                     destination_pdf="Output/destination"):
    """
    Function fill data into specific position of original pdf, generate new pdf file with data filled.
    @param position: a dictionary described the positions 2-dim (x, y) that Each parameter(eg.. x) represent as a list.
           'position_x': [], 'position_y': []
    @param data_to_fill: a list include all data need to be filled into pdf. Must be assigned relevant position.
    @param original_pdf: The pdf to be filled.
    @param destination_pdf: generate new pdf.
    @return: no defined.
    """
    if os.path.exists(destination_pdf):
        os.remove(destination_pdf)
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    for i in range(len(position['position_x'])):
        can.drawString(int(position['position_x'][i]), int(position['position_y'][i]), data_to_fill[i])
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(original_pdf, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real
    current = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    destination_pdf = destination_pdf+'_'+current+'.pdf'
    outputStream = open(destination_pdf, "wb")
    output.write(outputStream)
    outputStream.close()

    return destination_pdf
