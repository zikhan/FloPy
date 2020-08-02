import wpf

from System.Windows import Window
from System.ComponentModel import BackgroundWorker

class refreshStatus(Window):

	totalValue = 0
	def __init__(self):
		wpf.LoadComponent(self, 'refreshStatus.xaml')
		pass
	
	def something(self):
		pass

	def setBarStatus(self, value):
		
		totalValue = value
		self.bar.Value = totalValue
		pass

	def barAutoClose(self):
			self.Close()
