import wpf

from System.Windows import Window

class LineTestSystem(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'LineTestSystem.xaml')
