@echo off
ipy pyc.py /main:..\sandBox.py ..\Window1.py ..\AboutWindow.py ..\EllipsePrompt.py ..\RectPrompt.py ..\ConPrompt.py ..\debugLog.py ..\ParaPrompt.py /out:flopy /target:winexe /standalone
copy ..\sandBox.xaml sandBox.xaml
copy ..\AboutWindow.xaml AboutWindow.xaml
copy ..\EllipsePrompt.xaml EllipsePrompt.xaml
copy ..\RectPrompt.xaml RectPrompt.xaml
copy ..\ConPrompt.xaml ConPrompt.xaml
copy ..\debugLog.xaml debugLog.xaml
copy ..\ParaPrompt.xaml ParaPrompt.xaml
copy ..\Window1.xaml Window1.xaml