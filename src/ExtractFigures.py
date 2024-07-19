import os
import shutil

import allure
import cv2
import numpy as np
import pandas as pd
import pdfminer
from PIL import Image
from allure_commons.types import AttachmentType
from configparser import ConfigParser
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

config_object = ConfigParser()
config_object.read("configurations.ini")
rootdir=os.getcwd()

def mse(img1, img2):
    try:
        h, w = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff ** 2)
        mse = err / (float(h * w))
        return mse, diff
    except:
        return 1.1,1.1


@allure.step("Extracting Images in PDF")
def pdf_images_extraction(pdfpath, outputdir):
    pageIndex = 0
    imageIndex = 0
    if os.path.exists(outputdir):
        shutil.rmtree(outputdir)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    with open(pdfpath, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            pageIndex = pageIndex + 1
            imageIndex = 0
            interpreter.process_page(page)
            layout = device.get_result()
            for figure in layout:
                if (isinstance(figure, pdfminer.layout.LTFigure)):
                    for image_object in figure:
                        if (isinstance(image_object, pdfminer.layout.LTImage)):
                            image = Image.frombytes('1', image_object.srcsize, image_object.stream.get_data(), 'raw')
                            name = image_object.name + '.jpg';
                            imageIndex = imageIndex + 1;
                            with open(outputdir + "\\" + str(pageIndex) + "_" + str(imageIndex) + '.jpg', 'wb') as fp:
                                image.save(fp);


@allure.step("Compare Images in PDF with the expected Images")
def compare_pdf_images(realImg_dir, expectedImg_dir):
    for images in os.listdir(realImg_dir):
        # check if the image ends with png
        if (images.endswith(".jpg") or images.endswith(".bmp")):
            img1 = cv2.imread(realImg_dir + "\\" + images)
            img2 = cv2.imread(expectedImg_dir + "\\" + images)

            # convert the images to grayscale
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            compare_pdf_logos(img1, img2, images, realImg_dir, expectedImg_dir,images.split("_")[0])
            # error, diff = mse(img1, img2)
            # if (error == 0.0):
            #     print("------------------------------------------------------------------------------")
            #     print("------------------           " + images + " - Matched           --------------")
            #     allure.attach.file(expectedImg_dir + "\\" + images, name="Expected Logo on PDF Page "+images.split("_")[0], attachment_type=AttachmentType.PNG);
            #     allure.attach.file(realImg_dir + "\\" + images, name="Actual Logo on PDF Page "+images.split("_")[0], attachment_type=AttachmentType.PNG);
            #     print("------------------------------------------------------------------------------")
            # else:
            #     print("Image matching Error between the two images:", error)
            #     allure.attach.file(expectedImg_dir + "\\" + images,
            #                        name="Expected Logo on PDF Page " + images.split("_")[0],
            #                        attachment_type=AttachmentType.PNG);
            #     allure.attach.file(realImg_dir + "\\" + images, name="Actual Logo on PDF Page " + images.split("_")[0],
            #                        attachment_type=AttachmentType.PNG);
@allure.step("Validating logos on PDF PageNumber {pageNumber}")
def compare_pdf_logos(img1,img2,images,realImg_dir,expectedImg_dir,pageNumber):
    error, diff = mse(img1, img2)
    if (error == 0.0):
        print("------------------------------------------------------------------------------")
        print("------------------           " + images + " - Matched           --------------")
        allure.attach.file(expectedImg_dir + "\\" + images, name="Expected Logo on PDF Page " + pageNumber,
                           attachment_type=AttachmentType.PNG);
        allure.attach.file(realImg_dir + "\\" + images, name="Actual Logo on PDF Page " + pageNumber,
                           attachment_type=AttachmentType.PNG);
        print("------------------------------------------------------------------------------")
    else:
        print("Image matching Error between the two images:", error)
        allure.attach.file(expectedImg_dir + "\\" + images,
                           name="Expected Logo on PDF Page " + images.split("_")[0],
                           attachment_type=AttachmentType.PNG);
        allure.attach.file(realImg_dir + "\\" + images, name="Actual Logo on PDF Page " + pageNumber,
                           attachment_type=AttachmentType.PNG);
    assert error == 0.0


def compare_pdf_signatures(realImg_dir,row,pageNumber,imageindex):
            assertioncheck=True;
            year=row["Content"].split("@")[1].split("-")[2]
            subfoldername=getSignaturesFolder(year)
            for eachsignature in row["Content"].split("@")[0].split(","):
                imageindex=imageindex+1;
                img1 = cv2.imread(rootdir+config_object["General"]["SignaturesFolder"] + "\\" + subfoldername+"\\"+eachsignature+".jpg")
                img2 = cv2.imread(realImg_dir + "\\" + str(row["Page"])+"_"+str(imageindex)+".jpg")

                img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                error, diff = mse(img1, img2)
                try:
                    compareSignatures(img1, img2, eachsignature, subfoldername, realImg_dir,imageindex,str(row["Page"]))
                except AssertionError:
                    assertioncheck=False
                    pass
            return assertioncheck
                # if (error == 0.0):
                #     print("------------------------------------------------------------------------------")
                #     print("------------------           " + eachsignature + " - Matched           --------------")
                #     allure.attach.file(rootdir+config_object["General"]["SignaturesFolder"] + "\\" + subfoldername+"\\"+eachsignature+".jpg", name=eachsignature+" in year range "+subfoldername,attachment_type=AttachmentType.PNG);
                #     allure.attach.file(realImg_dir + "\\" + str(row["Page"])+"_"+str(imageindex)+".jpg", name=eachsignature+" on PDF",attachment_type=AttachmentType.PNG);
                #     print("------------------------------------------------------------------------------")
                # else:
                #     print("Image matching Error between the two images:", error)
                #     allure.attach.file(rootdir + config_object["General"]["SignaturesFolder"] + "\\" + subfoldername + "\\" + eachsignature + ".jpg",
                #                        name=eachsignature + " in year range " + subfoldername,
                #                        attachment_type=AttachmentType.PNG);
                #     allure.attach.file(realImg_dir + "\\" + str(row["Page"]) + "_" + str(imageindex) + ".jpg",
                #                        name=eachsignature + " on PDF", attachment_type=AttachmentType.PNG);

@allure.step("Validating Signature of  {eachsignature} in PDF, Year range {subfoldername}, PDF page number {pageNumber}")
def compareSignatures(img1,img2,eachsignature,subfoldername,realImg_dir,imageindex,pageNumber):
    error, diff = mse(img1, img2)
    if (error == 0.0):
        print("------------------------------------------------------------------------------")
        print("------------------           " + eachsignature + " - Matched           --------------")
        allure.attach.file(rootdir + config_object["General"][
            "SignaturesFolder"] + "\\" + subfoldername + "\\" + eachsignature + ".jpg",
                           name="Expected "+eachsignature + " in year range " + subfoldername, attachment_type=AttachmentType.PNG);
        allure.attach.file(realImg_dir + "\\" + str(pageNumber) + "_" + str(imageindex) + ".jpg",
                           name="Actual "+eachsignature + " on PDF", attachment_type=AttachmentType.PNG);
        print("------------------------------------------------------------------------------")
    else:
        print("------------------------------------------------------------------------------")
        print("------------------           " + eachsignature + " - Not Matched           --------------")
        print("Image matching Error between the two images:", error)
        allure.attach.file(rootdir + config_object["General"][
            "SignaturesFolder"] + "\\" + subfoldername + "\\" + eachsignature + ".jpg",
                           name="Expected "+eachsignature + " in year range " + subfoldername,
                           attachment_type=AttachmentType.PNG);
        allure.attach.file(realImg_dir + "\\" + str(pageNumber) + "_" + str(imageindex) + ".jpg",
                           name="Actual "+eachsignature + " on PDF", attachment_type=AttachmentType.PNG);
        print("------------------------------------------------------------------------------")
    assert error == 0.0

def getSignaturesFolder(year):
    subfolders = [f.name for f in os.scandir(rootdir+config_object["General"]["SignaturesFolder"]) if f.is_dir()]
    for eachsubfolder in subfolders:
        if(int(eachsubfolder.split("-")[0])<=int(year) and int(eachsubfolder.split("-")[1])>=int(year)):
            return eachsubfolder;
