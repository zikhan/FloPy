import clr
clr.AddReference('IronPython.Wpf')

import wpf

from System.Windows import Window

class EllipsePrompt(Window):
	def __init__(self):
		wpf.LoadComponent(self, 'EllipsePrompt.xaml')
		pass

	def disableForm(self, sender, e):
		self.funcNamePanel.IsEnabled = False
		self.variablePanel.IsEnabled = False
		pass

	def enableForm(self, sender, e):
		self.funcNamePanel.IsEnabled = True
		self.variablePanel.IsEnabled = True
		pass

	def buttonOk_click(self, sender, e):
		self.DialogResult = True
		pass
