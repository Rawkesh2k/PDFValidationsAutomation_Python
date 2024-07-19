import os
from configparser import ConfigParser

import pandas as pd

from src.ExtractFigures import pdf_images_extraction, compare_pdf_images, compare_pdf_signatures
from src.ValidateText import validate_static_dynamic_text_pdf, validate_dynamic_text_pdf, attachPDF

config_object = ConfigParser()
config_object.read("configurations.ini")
simpleUseCaseInfo = config_object["TextValidation_Complex"]
rootdir=os.getcwd()

def test_complex_PDF_Attachment_Annuity_Certificate():
    attachPDF(rootdir + config_object["PDFPath_Complex"]["pdfpath"])

def test_complex_Annuity_Certificates_Static_Text_Validations():
    validate_static_dynamic_text_pdf(rootdir+config_object["PDFPath_Complex"]["pdfpath"],
                                     rootdir+simpleUseCaseInfo["inputdataexcelpath"])

def test_complex_Annuity_Certificates_Dynamic_Data_Validations():
    testresult = True
    df = pd.read_excel(rootdir + simpleUseCaseInfo["inputdataexcelpath"])
    for index, row in df.iterrows():
        try:
            if row["TextType"] == 'Dynamic':
                validate_dynamic_text_pdf(rootdir+config_object["PDFPath_Complex"]["pdfpath"],
                                     row, row["Page"])
        except AssertionError:
            testresult = False
            pass
    assert testresult

def test_complex_Annuity_Certificates_Signatures_Validations():
    pdf_images_extraction(rootdir + config_object["PDFPath_Complex"]["pdfpath"],
                          rootdir + config_object["ImageValidation_Complex"]["actualimages"])

    df = pd.read_excel(rootdir+simpleUseCaseInfo["inputdataexcelpath"])

    for index, row in df.iterrows():
        imageindex=0;
        try:
        # Static Content Validation
            if row["TextType"] == 'Signatures':
                testresult=compare_pdf_signatures(rootdir + config_object["ImageValidation_Complex"]["actualimages"],
                                     row, row["Page"],imageindex)
        except AssertionError:
            testresult = False
            pass
    assert testresult