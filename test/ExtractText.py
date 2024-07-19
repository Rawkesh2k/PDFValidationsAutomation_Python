from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextBox, LTTextLine, LTText, LAParams, LTFigure

for page_layout in extract_pages("D:\\Venkata_Details\\PDFMInerProject\\RealPDF.pdf"):
    for element in page_layout:
        print(type(element))
        if isinstance(element, LTTextBox):
            print("------------>>>>>>>>>>>>>>> LTTextBox <<<<<<<<<<<<<------------------- ")
            print(element.get_text())
        # if isinstance(element, LTTextLine):
        #     print("------------>>>>>>>>>>>>>>> LTTextLine <<<<<<<<<<<<<------------------- ")
        #     print(element.get_text())
        # if isinstance(element, LTText):
        #     print("------------>>>>>>>>>>>>>>> LTText <<<<<<<<<<<<<------------------- ")
        #     print(element.get_text())
        # if isinstance(element,LTTextContainer):
        #     print("------------>>>>>>>>>>>>>>> LTTextContainer <<<<<<<<<<<<<------------------- ")
        #     print(element.get_text())
        # if isinstance(element,LTFigure):
        #     print("------------>>>>>>>>>>>>>>> LTFigure <<<<<<<<<<<<<------------------- ")
        #     print(element.group_textlines())