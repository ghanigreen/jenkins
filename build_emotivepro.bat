set build_id=%1
call C:\"Program Files (x86)"\"Microsoft Visual Studio 14.0"\VC\vcvarsall.bat x64
cd C:\Jenkins\workspace\EmotivPro\build-Emotiv-Desktop_Qt_5_7_1_MSVC2015_32bit2-Debug
C:\Qt\5.7\msvc2015_64\bin\qmake.exe C:\Jenkins\workspace\EmotivPro\EmotivPro\Emotiv.pro -spec win32-msvc2015 "CONFIG+=debug" "CONFIG+=qml_debug
C:\Qt\Tools\QtCreator\bin\jom.exe
C:\Qt\5.7\msvc2015_64\bin\windeployqt.exe --qmldir C:\Jenkins\workspace\EmotivPro\EmotivPro\qmlcomponents .\debug\Emotiv.exe
::.\debug\Emotiv.exe
mkdir C:\Jenkins\workspace\EmotivPro\build-jenkin-%build_id%
xcopy /s C:\Jenkins\workspace\EmotivPro\build-Emotiv-Desktop_Qt_5_7_1_MSVC2015_32bit2-Debug\debug C:\Jenkins\workspace\EmotivPro\build-jenkin-%build_id%