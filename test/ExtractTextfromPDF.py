from pdfminer.high_level import extract_text

from src.ValidateText import getIndexedContent

for i in range(38):
    print("---------------------->>>>>>>>>> Page: "+str(i+1)+"<<<<<<<<<<<<<<<<----------------------------")
    print(extract_text("W:\\Photon\\Python_Workspace\\PDFMInerProject\\pdf\\Complex\\ComplexPDF.pdf", "", [i]))

# print(getIndexedContent(extract_text("W:\\Photon\\Python_Workspace\\PDFMInerProject\\pdf\\Medium\\MediumPDF1.pdf", "", [86])))