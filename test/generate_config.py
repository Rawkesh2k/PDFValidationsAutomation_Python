import configparser
import os

config_file = configparser.ConfigParser()

config_file.add_section("TextValidation_Simple")
config_file.set("TextValidation_Simple", "inputDataExcelPath", os.getcwd()+"\\TextData\\Simple\\TextValidations.xlsx")

config_file.add_section("TextValidation_Medium")
config_file.set("TextValidation_Medium", "inputDataExcelPath", os.getcwd()+"\\TextData\\Medium\\TextValidations.xlsx")

config_file.add_section("TextValidation_Complex")
config_file.set("TextValidation_Complex", "inputDataExcelPath", os.getcwd()+"\\TextData\\Complex\\TextValidations.xlsx")

config_file.add_section("ImageValidation_Simple")
config_file.set("ImageValidation_Simple", "ActualImages", os.getcwd()+"\\Images\\Simple\\Actual")
config_file.set("ImageValidation_Simple", "ExpectedImages", os.getcwd()+"\\Images\\Simple\\Expected")

config_file.add_section("ImageValidation_Medium")
config_file.set("ImageValidation_Medium", "ActualImages", os.getcwd()+"\\Images\\Medium\\Actual")
config_file.set("ImageValidation_Medium", "ExpectedImages", os.getcwd()+"\\Images\\Medium\\Expected")

config_file.add_section("ImageValidation_Complex")
config_file.set("ImageValidation_Complex", "ActualImages", os.getcwd()+"\\Images\\Complex\\Actual")
config_file.set("ImageValidation_Complex", "ExpectedImages", os.getcwd()+"\\Images\\Complex\\Expected")


with open(r"../configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

