import os
import shutil
import cv2

import numpy as np
import pdfminer
from pdfminer.image import ImageWriter
from pdfminer.high_level import extract_pages

pages = list(extract_pages("/RealPDF.pdf"))
pageIndex=0;
imageIndex=0;
def get_image(layout_object):
    global imageIndex;
    if isinstance(layout_object, pdfminer.layout.LTImage):
        imageIndex = imageIndex + 1;
        return layout_object
    if isinstance(layout_object, pdfminer.layout.LTContainer):
        for child in layout_object:
            return get_image(child)
    else:
        return None

def mse(img1, img2):
   h, w = img1.shape
   diff = cv2.subtract(img1, img2)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse, diff

def save_images_from_page(page: pdfminer.layout.LTPage):
    global imageIndex;
    imageIndex=0;
    images = list(filter(bool, map(get_image, page)))
    iw = ImageWriter('output_img')
    for image in images:
        name=iw.export_image(image)
        os.rename('output_img\\'+name, 'output_img\\'+str(pageIndex) +"-" + str(imageIndex)+"." +name.split(".")[len(name.split("."))-1])
#

if os.path.exists('output_img'):
    shutil.rmtree('output_img')
for page in pages:
    pageIndex=pageIndex+1;
    save_images_from_page(page)

realImg_dir = "W:\\Photon\\Python_Workspace\\PDFMInerProject\\RealImages"
expectedImg_dir="output_img"
for images in os.listdir(realImg_dir):
    # check if the image ends with png
    if (images.endswith(".jpg") or images.endswith(".bmp")):
        img1 = cv2.imread("W:\\Photon\\Python_Workspace\\PDFMInerProject\\RealImages\\"+images)
        img2 = cv2.imread("W:\\Photon\\Python_Workspace\\PDFMInerProject\\output_img\\"+images)

        # convert the images to grayscale
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        error, diff = mse(img1, img2)
        print("Image matching Error between the two images:", error)

        cv2.imshow("difference", diff)
        cv2.waitKey(0)
        cv2.destroyAllWindows()




