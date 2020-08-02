import clr
clr.AddReference('IronPython.Wpf')

import wpf

from System.Windows import Window, Controls, Thickness, VerticalAlignment, HorizontalAlignment, NameScope
class RectPrompt(Window):
	returnText = []
	totalTextBoxes = 1
	def __init__(self):
		wpf.LoadComponent(self, 'RectPrompt.xaml')
		totalTextBoxes = 1
		returnText = []
		pass

	def buttonOk_click(self, sender, e):
		self.returnText = []
		for i in self.Procedure.Children:
			if len(i.Text) != 0:
				if i == self.Procedure.Children[0]:
					self.returnText.append(i.Text)
					pass
				else:
					appendText = "\n"
					appendText += i.Text
					self.returnText.append(appendText)
					pass
				pass
		self.DialogResult = True
		pass

	def newLine(self, sender, e):

		tb = Controls.TextBox()
		tb.Padding = Thickness(5)
		tb.Margin = Thickness(20,5,20,0)
		tb.VerticalAlignment = VerticalAlignment.Center
		tb.HorizontalAlignment = HorizontalAlignment.Left
		tb.AutoWordSelection = True
		tb.MaxLines = 1
		tb.VerticalContentAlignment = VerticalAlignment.Center
		tb.MinWidth = 455
		tb.Text = ""

		self.Procedure.Children.Add(tb)
		self.totalTextBoxes += 1
		pass

	def window_opened(self, sender,e):
		self.returnText = []
		pass