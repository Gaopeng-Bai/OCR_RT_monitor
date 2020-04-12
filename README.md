# OCR-Video-Automation

This project extracts the picture area at the specified position in the video, recognizes the characters in the image and prints to the specified position in the pdf file. 

I provided a [simulator](https://github.com/Gaopeng-Bai/OCR_Simulator.git) developed by Csharp on windows form environments that can help to test this application, in additional a Real-time result present client named as ```Monitor_receiver``` included.

## Requirements

Before running this program, the local OS need to install several plugins to support this software.

* [pytesseract](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.0.0-beta.1.20180414.exe) is OCR LSTM engine to be installed for recognition.

* [Imagemagic](http://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-on-windows) to convert pdf file to image and additional image processing function.

* [ghostscript](https://www.ghostscript.com/download/gsdnld.html) only for solving the bugs during the image converter.

* Check the requirement file to install the package needed.

## Usage

 Run on single operation.

    ```
    python OCR_mian.py
    ```
 
### 1. Video Resource

* The default video stream comes from the local camera. 
