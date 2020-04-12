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

 Run Main GUI:

    python OCR_main.py

 ### 1. Video Resource

* The default video stream is the local camera. 

* For remote video stream, this app currently tested only on the RSTP protocol of [M1054](https://www.axis.com/products/axis-m1054) IP camera. *First*, click the remote camera of the menu bar to active entry of input of IP address and port. Second, enter the RTSP IP address and port of your IP camera, then click *connect* button.

 ### 2. Recognition area selection

 * Press left button of the mouse and draw an area that needs to be recognized. Then right button of the mouse to confirm your selection, pop-up windows will be show to collect the name of this area.

 * In addition to managing the boxes of area. Simply click the menu button, select one item to operate (button or keyboard shortcut: "F2" for Rename and "Delete" for delete )

 ### 3. Output to file

 * Select the PDF file to receive the recognition result.

 * Drop down the box name and select one item, then click the button to set up the PDF position be to print the recognition result of this item. 

 * Set all items to relevant PDF position.

 ### 4. Run the recognition program

 * Run a single operation show this result on your default PDF viewer.

 * Set a timer to automatically generate the result and present on the remote application in [Monitor_receiver](https://github.com/Gaopeng-Bai/OCR_Simulator.git). Be sure to run ``Monitor_receiver`` before timer of Main GUI running.
 