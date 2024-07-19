from pdfminer.layout import LAParams, LTTextBox, LTText, LTChar, LTAnno
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import PDFPageAggregator

#Imports Searchable PDFs and prints x,y coordinates
fp = open('D:\\Venkata_Details\\PDFMInerProject\\RealPDF.pdf', 'rb')
manager = PDFResourceManager()
laparams = LAParams()
dev = PDFPageAggregator(manager, laparams=laparams)
interpreter = PDFPageInterpreter(manager, dev)
pages = PDFPage.get_pages(fp)

for page in pages:
    print('--- Processing ---')
    interpreter.process_page(page)
    layout = dev.get_result()
    x, y, text = -1, -1, ''
    for textbox in layout:
        if isinstance(textbox, LTText):
          for line in textbox:
            for char in line:
              # If the char is a line-break or an empty space, the word is complete
              if isinstance(char, LTAnno) or char.get_text() == ' ':
                if x != -1:
                  print('At %r is text: %s' % ((x, y), text))
                x, y, text = -1, -1, ''
              elif isinstance(char, LTChar):
                text += char.get_text()
                if x == -1:
                  x, y, = char.bbox[0], char.bbox[3]
    # If the last symbol in the PDF was neither an empty space nor a LTAnno, print the word here
    if x != -1:
      print('At %r is text: %s' % ((x, y), text))
    break