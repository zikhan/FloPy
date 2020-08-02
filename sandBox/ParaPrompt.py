import clr
clr.AddReference('IronPython.Wpf')

import wpf

from System.Windows import Window, Visibility
from System.Windows.Controls import *
from Microsoft.Win32 import OpenFileDialog


#Names of Grids:
#UInput, Printer, Opener, Read1, Writer, ReadMany
#
class ParaPrompt(Window):
	Grids = []
	Sel = 0
	returnText = ""
	def __init__(self):
		wpf.LoadComponent(self, 'ParaPrompt.xaml')
		pass

	def window_Opened(self, sender, e):
		self.Grids = [self.UInput, self.Printer, self.Opener, self.Read1, self.ReadMany, self.Writer] #DO NOT CHANGE THIS ORDER, UNLESS YOU WANT TO SCREW UP THE PROMPT
		self.returnText = ""
		pass

	def buttonOk_click(self, sender, e):
		self.returnText = ""
		self.tempStore.Text = ""
		self.Sel = self.mainCombo.SelectedIndex
		if (self.Sel == 0):
			returnText = self.UInput_Ret()
			pass
		elif (self.Sel == 1):
			returnText = self.Printer_Ret()
			pass
		elif (self.Sel == 2):
			returnText = self.Opener_Ret()
			pass
		elif (self.Sel == 3):
			returnText = self.Read1_Ret()
			pass
		elif (self.Sel == 4):
			returnText = self.ReadMany_Ret()
			pass
		elif (self.Sel == 5):
			returnText = self.Writer_Ret()
			pass
		self.tempStore.Text = returnText
		self.DialogResult = True
		pass

	def UInput_Sel(self, sender, e):
		#index0
		self.setVisibility(0)
		self.Sel = 0
		pass

	def UInput_Ret(self):
		#save variable is called saveVarName
		#prompt for input is called prompt
		a = self.saveVarName.Text
		b = self.prompt.Text

		tex = "{} = input(\"{}\")".format(a,b)

		#return a string
		return tex

	def Printer_Sel(self, sender, e):
		#index1
		self.setVisibility(1)
		self.Sel = 1
		pass

	def Printer_Ret(self):
		#print statement is called printStat
		a = self.printStat.Text

		tex = "print({})".format(a)
		#return a string
		return tex

	def Opener_Sel(self, sender, e):
		#index2
		self.setVisibility(2)
		self.Sel = 2
		pass

	def Opener_Ret(self):
		#File address is called fileLoc
		#open type combobox is called openType
		#file object variable is called varFileName
		a = self.fileLoc.Text

		opentype = ComboBoxItem()
		opentype = self.openType.SelectedItem
		b = opentype.Content.ToString()

		c = self.varFileName.Text

		tex = "{} = open(\"{}\",\"{}\")".format(c, a, b)
		#return a string
		return tex

	def Read1_Sel(self, sender, e):
		#index3
		self.setVisibility(3)
		self.Sel = 3
		pass

	def Read1_Ret(self):
		#The file object to read from is called FOVar
		#The memLoc to stored the info is called VarStore
		a = self.FOVar.Text
		b = self.VarStore

		tex = "{} = {}.readline()".format(b,a)
		#return a string
		return tex

	def ReadMany_Sel(self, sender, e):
		#index4
		self.setVisibility(4)
		self.Sel = 4
		pass

	def ReadMany_Ret(self):
		#The file object to read from is called rFOVar
		#The stack to store it in is called arrStore
		a = self.rFOVar.Text
		b = self.arrStore.Text

		tex = "{} = {}.readlines()".format(b,a)
		#return a string
		return tex

	def Writer_Sel(self, sender, e):
		#index5
		self.setVisibility(5)
		self.Sel = 5
		pass
	
	def Writer_Ret(self):
		#File object to write to is called wFOVar
		#stuff to write is called writeThis
		a = self.wFOVar.Text
		b = self.writeThis.Text

		tex = "{}.write(\"{}\")".format(a,b)
		#return a string
		return tex

	def setVisibility(self, index):
		for i in range(len(self.Grids)):
			if (index == i):
				self.Grids[i].Visibility = Visibility.Visible
			else:
				self.Grids[i].Visibility = Visibility.Collapsed
		pass

	def browseFile(self, sender, e):
		file = OpenFileDialog()

		result = file.ShowDialog()

		if result:
			self.fileLoc.Text = file.FileName
		pass
