del /s /q /f C:\Jenkins\workspace\EDK_Auto_Test\*.xml
C:\Jenkins\workspace\EDK_Auto_Test\SdkAutoTest\bin\x86\ActivateLicense.exe --log_level=all --report_level=no --log_format=XML --log_sink=result1.xml
C:\Jenkins\workspace\EDK_Auto_Test\SdkAutoTest\bin\x86\AverageBandPowers.exe --log_level=all --report_level=no --log_format=XML --log_sink=result2.xml
::C:\Jenkins\workspace\EDK_Auto_Test\SdkAutoTest\bin\x86\HeadsetInformationLogger.exe --log_level=all --report_level=no --log_format=XML --log_sink=result2.xml
::C:\Jenkins\workspace\EDK_Auto_Test\SdkAutoTest\bin\x86\MultiDongleConnection.exe --log_level=all --report_level=no --log_format=XML --log_sink=result3.xml
::C:\Jenkins\workspace\EDK_Auto_Test\SdkAutoTest\bin\x86\SavingAndLoadingProfileCloud.exe --log_level=all --report_level=no --log_format=XML --log_sink=result4.xml