mkdir out
cp 'C:\Program Files\IronPython 2.7\DLLs\IronPython.Wpf.dll' .\out\
ipyc /main:.\sandBox\sandBox.py .\sandBox\Window1.py .\sandBox\AboutWindow.py .\sandBox\EllipsePrompt.py .\sandBox\RectPrompt.py .\sandBox\ConPrompt.py .\sandBox\debugLog.py .\sandBox\ParaPrompt.py 'C:\Program Files\IronPython 2.7\Lib\wpf.py' /out:.\out\flopy /target:winexe /standalone /win32icon:'.\sandBox\Resources\floPy Icon.ico'
mv .\flopy.exe .\out\ -Force
cp .\sandBox\*.xaml .\out\
mkdir out\Resources
cp '.\sandBox\Resources\floPy Icon.ico' .\out\Resources\
