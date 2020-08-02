import clr
clr.AddReference('IronPython.Wpf')


import wpf

from System.Windows import Window
from System.Diagnostics import Process
from Window1 import Window1

class AboutWindow(Window):
	def __init__(self):
		wpf.LoadComponent(self, 'AboutWindow.xaml')
		num2 = Window1()
		num2.Show()
		pass

	def Button_Click(self, sender, e):
		self.Close()
		pass

	def Hyperlink_Click(self, sender, e):
		Process.Start('http://zovink.com')
		pass
