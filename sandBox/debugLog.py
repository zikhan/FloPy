import clr
clr.AddReference('IronPython.Wpf')

import wpf

from System.Windows import Window

class debugLog(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'debugLog.xaml')
