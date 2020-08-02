import wpf

from System.Windows import Window

class tutorialWindow(Window):

	step = 0
	def __init__(self):
		wpf.LoadComponent(self, 'tutorialWindow.xaml')
		pass
