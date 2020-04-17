@ECHO OFF
:: Batch file to generate exe-file
:: TODO: Reimplement without absolute paths
::
:: Josef Andersson April 2020

C:
cd C:\Users\joffa\PycharmProjects\sugarmate2nightscout\sugarmate2nightscout\
C:\Users\joffa\PycharmProjects\sugarmate2nightscout\venv\Scripts\pyinstaller.exe -y --onefile sync_data.py