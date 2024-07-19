import os
from configparser import ConfigParser

import pandas as pd

from src.ExtractFigures import pdf_images_extraction, compare_pdf_images
from src.ValidateText import validate_static_dynamic_text_pdf, validate_dynamic_text_pdf, attachPDF

config_object = ConfigParser()
config_object.read("configurations.ini")
simpleUseCaseInfo = config_object["TextValidation_Medium"]
rootdir=os.getcwd()

def test_medium_PDF_Attachment_Brokerage_Account_Opening():
    attachPDF(rootdir+config_object["PDFPath_Medium"]["pdfpath"])

def test_medium_Brokerage_Account_Opening_Static_Text_Validations():
    validate_static_dynamic_text_pdf(rootdir+config_object["PDFPath_Medium"]["pdfpath"],
                                     rootdir+simpleUseCaseInfo["inputdataexcelpath"])

def test_medium_Brokerage_Account_Opening_Dynamic_Data_Validations():
    testresult = True
    df = pd.read_excel(rootdir + simpleUseCaseInfo["inputdataexcelpath"])
    for index, row in df.iterrows():
        try:
            if row["TextType"] == 'Dynamic':
                validate_dynamic_text_pdf(rootdir + config_object["PDFPath_Medium"]["pdfpath"],
                                               row, row["Page"])
        except AssertionError:
            testresult = False
            pass
    assert testresult

def test_medium_Brokerage_Account_Opening_Logos_Validations():
    pdf_images_extraction(rootdir + config_object["PDFPath_Medium"]["pdfpath"],
                          rootdir + config_object["ImageValidation_Medium"]["actualimages"])
    compare_pdf_images(rootdir + config_object["ImageValidation_Medium"]["actualimages"],
                       rootdir + config_object["ImageValidation_Medium"]["expectedimages"])