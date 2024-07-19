W:
cls
cd W:\Photon\Python_Workspace\PDFMInerProject
python -m pytest --alluredir=Reports
allure serve W:\Photon\Python_Workspace\PDFMInerProject\Reports
allure generate --clean --output W:\Photon\Python_Workspace\PDFMInerProject\Reports
cmd.exe
