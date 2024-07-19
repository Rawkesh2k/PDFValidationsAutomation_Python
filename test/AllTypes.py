from pdfminer.high_level import extract_pages
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1

from test.PDFTextValidation import interpreter, pages

for pagenumber,page_layout in enumerate(extract_pages("W:\\Photon\\Python_Workspace\\PDFMInerProject\\pdf\\Complex\\ComplexPDF.pdf")):
    print("-------------->>>>>>>>>>>"+str(pagenumber)+"<<<<<<<<<<-------------------")
    for element in page_layout:
         print(type(element))

input_file_path="W:\\Photon\\Python_Workspace\\PDFMInerProject\\pdf\\Complex\\ComplexPDF.pdf";
input_file = open(input_file_path, 'rb')
input_parser = PDFParser(input_file)
input_document = PDFDocument(input_parser)
total_pages = resolve1(input_document.catalog['Pages'])['Count']
print(total_pages)

for index,page in enumerate(pages):
    interpreter.process_page(page)
    layout = dev.get_result()
    print("----------->>>>>>>>>>>>>"+str(index)+"<<<<<<<<<<<<<--------------------")
    paragrapghtext="";
    for textbox in layout:
        if isinstance(textbox, LTTextBox):
            paragrapghtext=paragrapghtext+textbox.get_text();
    print(paragrapghtext)