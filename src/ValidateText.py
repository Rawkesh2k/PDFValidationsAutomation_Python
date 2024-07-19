import allure
import pandas as pd
from allure_commons.types import AttachmentType
from pdfminer.high_level import extract_text

def difference(string1, string2):
    # Split both strings into list items
    string1 = string1.split()
    string2 = string2.split()

    A = set(string1)  # Store all string1 list items in set A
    B = set(string2)  # Store all string2 list items in set B

    str_diff = A.symmetric_difference(B)
    isEmpty = (len(str_diff) == 0)

    if isEmpty:
        print("No Difference. Both Strings Are Same")
    else:
        print("The Difference Between Two Strings: ")
        print(str_diff)

    print('The programs runs successfully.')


def getIndexedContent(text):
    Dict = {}
    index = 0
    for textline in text.split("\n"):
        if (textline != ""):
            Dict[index] = textline;
            index = index + 1;
    return Dict;

@allure.step("Expand below for Source PDF")
def attachPDF(path):
    allure.attach.file(path,name=path.split("\\")[len(path.split("\\"))-1], attachment_type=AttachmentType.PDF);

@allure.step("Validating Static Text in PDF")
def validate_static_dynamic_text_pdf(pdfpath, ExcelDatapath):
    df = pd.read_excel(ExcelDatapath)

    for index, row in df.iterrows():
        text = extract_text(pdfpath, "", [row["Page"] - 1])

        # Static Content Validation
        if row["TextType"] == 'Static':
            print("------------------->>>>>>>>> Validating Static Text on Page" + str(
                row["Page"]) + "<<<<<<<<<<----------------------")
            print()
            staticText = row["Content"]
            print("------------------------------------------------------------------------------")
            print("------------------       Static Text retrieved From PDF         --------------")
            print("------------------------------------------------------------------------------")
            print(text.encode("utf-8"))
            print()
            compare_static_Text(text,staticText,str(row["Page"]))

@allure.step("Validate Static Text on PDF Page: '{PDFPageNumber}'")
def compare_static_Text(staticTextfromPDF,expectedstaticTextinPDF,PDFPageNumber):
            if (staticTextfromPDF.find(expectedstaticTextinPDF) > -1):
                print("------------------------------------------------------------------------------")
                print("Static Text Validation on Page:" + PDFPageNumber + " is Successful")
                with allure.step("Static Text Validation on Page: {}  is Successful".format(PDFPageNumber)):
                    pass
                print("------------------------------------------------------------------------------")
            else:
                print("------------------------------------------------------------------------------")
                print("Static Text Validation on Page:" + PDFPageNumber + " is Not Successful")
                with allure.step("Static Text Validation on Page: {}  is Not Successful".format(PDFPageNumber)):
                    pass
                print("------------------------------------------------------------------------------")


@allure.step("Validating Dynamic Text in PDFPage {pageNumber}")
def validate_dynamic_text_pdf(pdfpath, row,pageNumber):

        if row["TextType"] == 'Dynamic':
            text = extract_text(pdfpath, "", [row["Page"] - 1])
            datafromPDF = getIndexedContent(text)
            print("------------------------------------------------------------------------------")
            print("-------------    Indexed Dynamic Text retrieved From PDF       ---------------")
            print("------------------------------------------------------------------------------")
            print(datafromPDF)
            print()
            DynamicDataMapping = eval(row["DynamicDataMapping"])
            for realdata in row["Content"].split(";"):
                if len(str(DynamicDataMapping[realdata.split(":")[0]]).split("-")) > 1:
                    Appendeddata = "";
                    for data in range(int(str(DynamicDataMapping[realdata.split(":")[0]]).split("-")[0]),
                                      int(str(DynamicDataMapping[realdata.split(":")[0]]).split("-")[1]) + 1):
                        Appendeddata = Appendeddata + datafromPDF[data];
                    compare_dynamic_content(realdata, Appendeddata,str(row["Page"]))
                    # if realdata.split(":")[1] == Appendeddata:
                    #     print("------------------------------------------------------------------------------")
                    #     print(
                    #         realdata.split(":")[0]+" - "+realdata.split(":")[1] + " is matching in both PDF and Excel page:" + str(row["Page"]))
                    #     allure.step(realdata.split(":")[1] + "is matching in both PDF and Excel page:" + str(row["Page"]))
                    #     print("------------------------------------------------------------------------------")
                    # else:
                    #     print("------------------------------------------------------------------------------")
                    #     print((realdata.split(":")[0]+" - "+realdata.split(":")[1] + "is Not matching in both PDF and Excel page:" + str(
                    #         row["Page"])))
                    #     print("Expected:" + realdata.split(":")[1])
                    #     print("Actual:" + Appendeddata)
                    #     print("------------------------------------------------------------------------------")
                else:
                    compare_dynamic_content(realdata,datafromPDF[int(str(DynamicDataMapping[realdata.split(":")[0]]))],str(
                            row["Page"]))
                    # if realdata.split(":")[1] == datafromPDF[int(str(DynamicDataMapping[realdata.split(":")[0]]))]:
                    #     print("------------------------------------------------------------------------------")
                    #     print(realdata.split(":")[0]+" - "+realdata.split(":")[1] + " is matching in both PDF and Excel on page:" + str(
                    #         row["Page"]))
                    #     print("------------------------------------------------------------------------------")
                    # else:
                    #     print("------------------------------------------------------------------------------")
                    #     print((realdata.split(":")[0]+" - "+realdata.split(":")[1] + " is Not matching in both PDF and Excel on page:" + str(
                    #         row["Page"])))
                    #     print("Expected:" + realdata.split(":")[1])
                    #     print("Actual:" + datafromPDF[int(str(DynamicDataMapping[realdata.split(":")[0]]))])
                    #     print("------------------------------------------------------------------------------")


@allure.step("Validate Dynamic Text Field {expectedDynamicData} on PDF Page: '{PDFPageNumber}'")
def compare_dynamic_content(expectedDynamicData,ActualDynamicData,PDFPageNumber):
    if expectedDynamicData.split(":",1)[1] == ActualDynamicData:
        print("------------------------------------------------------------------------------")
        print(expectedDynamicData.split(":")[0] + " - " + expectedDynamicData.split(":")[
            1] + " is matching in both PDF and Excel on page:" + PDFPageNumber)
        print("------------------------------------------------------------------------------")
    else:
        print("------------------------------------------------------------------------------")
        print((expectedDynamicData.split(":")[0] + " - " + expectedDynamicData.split(":")[
            1] + " is Not matching in both PDF and Excel on page:" + PDFPageNumber))
        print("Expected:" + expectedDynamicData.split(":")[1])
        print("Actual:" + ActualDynamicData)
        print("------------------------------------------------------------------------------")

    assert expectedDynamicData.split(":",1)[1]==ActualDynamicData

# python -m pytest --alluredir=Reports
# allure generate --clean --output W:\Photon\Python_Workspace\PDFMInerProject\Reports
# allure serve W:\Photon\Python_Workspace\PDFMInerProject\Reports
