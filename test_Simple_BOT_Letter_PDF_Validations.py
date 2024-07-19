import os
from configparser import ConfigParser

import pandas as pd

from src.ExtractFigures import pdf_images_extraction, compare_pdf_images
from src.ValidateText import validate_static_dynamic_text_pdf, validate_dynamic_text_pdf, attachPDF

config_object = ConfigParser()
config_object.read("configurations.ini")
rootdir=os.getcwd()


def test_simple_PDF_Attachment_BOT_Letter():
    attachPDF(rootdir+config_object["PDFPath_Simple"]["pdfpath"])

def test_easy_BOT_Letter_Stattic_Text_Validation():
    validate_static_dynamic_text_pdf(rootdir+config_object["PDFPath_Simple"]["pdfpath"],
                                     rootdir+config_object["TextValidation_Simple"]["inputdataexcelpath"])

def test_easy_BOT_Letter_User_Info_Dynamic_Text_Validation():
    testresult = True
    df = pd.read_excel(rootdir + config_object["TextValidation_Simple"]["inputdataexcelpath"])
    for index, row in df.iterrows():
        try:
            if row["TextType"] == 'Dynamic':
                validate_dynamic_text_pdf(rootdir + config_object["PDFPath_Simple"]["pdfpath"],
                                     row, row["Page"])
        except AssertionError:
            testresult = False
            pass
    assert testresult

def test_easy_BOT_Letter_Logos_Validation():
    pdf_images_extraction(rootdir + config_object["PDFPath_Simple"]["pdfpath"],
                          rootdir + config_object["ImageValidation_Simple"]["actualimages"])
    compare_pdf_images(rootdir + config_object["ImageValidation_Simple"]["actualimages"],
                       rootdir + config_object["ImageValidation_Simple"]["expectedimages"])