from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from pdfminer.layout import LAParams, LTTextBox, LTText, LTChar, LTAnno
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import PDFPageAggregator

fp = open('W:\\Photon\\Python_Workspace\\PDFMInerProject\\pdf\\Complex\\ComplexPDF.pdf', 'rb')
manager = PDFResourceManager()
laparams = LAParams()
dev = PDFPageAggregator(manager, laparams=laparams)
interpreter = PDFPageInterpreter(manager, dev)
pages = PDFPage.get_pages(fp)

for index,page in enumerate(pages):
    interpreter.process_page(page)
    layout = dev.get_result()
    print("----------->>>>>>>>>>>>>"+str(index)+"<<<<<<<<<<<<<--------------------")
    paragrapghtext="";
    for textbox in layout:
        if isinstance(textbox, LTTextBox):
            paragrapghtext=paragrapghtext+textbox.get_text();
    print(paragrapghtext)

# for pagenumber,page_layout in enumerate(extract_pages("W:\\Photon\\Python_Workspace\\PDFMInerProject\\pdf\\Complex\\ComplexPDF.pdf")):
#      text=""
#      for element in page_layout:
#          if isinstance(element, LTTextContainer) :
#             text=text+element.get_text();
#      print("----------->>>>>>>>>>>>>" + str(pagenumber) + "<<<<<<<<<<<<<<--------------------")
#      print(text)