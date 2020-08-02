import clr
clr.AddReference('IronPython.Wpf')
clr.AddReference('System.Xml')

import wpf

from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Shapes import *
from System.Windows.Media import *
from Microsoft.Win32 import *
from System.Windows.Input import *
from System.IO import StringReader
from System.Xml import XmlTextReader

from AboutWindow import AboutWindow
from EllipsePrompt import EllipsePrompt
from RectPrompt import RectPrompt
from ParaPrompt import ParaPrompt
from debugLog import debugLog
from ConPrompt import ConPrompt

DEBUG = False
me = Application()

class MyWindow(Window):
	dbugWin =  debugLog()
	OpenFile = ''
	isUnderFunc = False

	def __init__(self):
		wpf.LoadComponent(self, 'sandBox.xaml')
		pass

	if DEBUG:
		dbugWin.Show()

	def createComponentGrid(self):	
		newGrid = Grid()
		newGrid.RowDefinitions.Add(RowDefinition()) #Row for Flow Name
		newGrid.RowDefinitions.Add(RowDefinition()) #Row for actual flow component
		newGrid.RowDefinitions.Add(RowDefinition()) #Row for variables affected

		return newGrid

	def createEndLine(self):
		arrow = Line()
		arrow.Y1 = 0
		arrow.Y2 = 1
		arrow.X1 = 0
		arrow.X2 = 0
		arrow.HorizontalAlignment = HorizontalAlignment.Center
		arrow.VerticalAlignment = VerticalAlignment.Bottom
		arrow.StrokeEndLineCap = PenLineCap.Square
		arrow.StrokeStartLineCap = PenLineCap.Square
		arrow.Stretch = Stretch.Fill
		arrow.Height = 20
		#arrow.Margin = Thickness(0,(20+objectHeight),0,0)
		arrow.Stroke = Brushes.Black
		arrow.StrokeThickness = 10

		return arrow
	
	def createStartLine(self):
		arrow = Line()
		arrow.Y1 = 0
		arrow.Y2 = 1
		arrow.X1 = 0
		arrow.X2 = 0
		arrow.HorizontalAlignment = HorizontalAlignment.Center
		arrow.VerticalAlignment = VerticalAlignment.Top
		arrow.StrokeEndLineCap = PenLineCap.Triangle
		arrow.StrokeStartLineCap = PenLineCap.Square
		arrow.Stretch = Stretch.Fill
		arrow.Height = 20
		#arrow.Margin = Thickness(0,0,0,(20 + objectHeight))
		arrow.Stroke = Brushes.Black
		arrow.StrokeThickness = 10

		return arrow
	
	curGridPosition = [0,0]
	def addNewRowObject(self, RowObject):
		rowDef = RowDefinition()
		rowDef.Height = GridLength(1,GridUnitType.Auto)
		rowDef.MinHeight = 80
		self.flowView.RowDefinitions.Add(rowDef)
		self.flowView.Children.Add(RowObject)
		#self.flowView.SetRow(RowObject,self.flowView.Children.IndexOf(RowObject))

		self.flowView.SetRow(RowObject,self.curGridPosition[0])
		self.curGridPosition[0] += 1
		self.writeDBugText("addNewRowObject -- IndexOf {} is {} ".format(RowObject.Name, self.flowView.Children.IndexOf(RowObject)))
		
		pass

	def CreateEllipseShape(self, func, vars, isEnd):
		#Create Actual Ellipse
		newEllipse = Ellipse()
		newEllipse.Height = 60
		newEllipse.Width = 100
		newEllipse.Fill = Brushes.CornflowerBlue
		newEllipse.Stroke = Brushes.Black
		newEllipse.StrokeThickness = 2.0
		newEllipse.HorizontalAlignment = HorizontalAlignment().Center
		newEllipse.VerticalAlignment = VerticalAlignment().Center
		#Create Grid
		ellipseGrid = self.createComponentGrid()
		ellipseGrid.HorizontalAlignment = HorizontalAlignment.Center
		ellipseGrid.VerticalAlignment = VerticalAlignment.Center
		ellipseGrid.Name = "Ellipse{}".format(self.totalEllipses)

		ellipseGrid.Children.Add(newEllipse) #Add newEllipse to the component grid
		ellipseGrid.SetRow(newEllipse,1) #Set the Row of the Ellipse to the middle row
		
		textblock = TextBlock()
		if isEnd:
			textblock.Text = "End"
			arrow = self.createStartLine()
			ellipseGrid.Children.Add(arrow)
			ellipseGrid.SetRow(arrow,0)
			pass
		else:
			textblock.Text = "Start"
			arrow = self.createEndLine()
			ellipseGrid.Children.Add(arrow)
			ellipseGrid.SetRow(arrow,2)
			textb = TextBlock()
			textb.FontSize = 9
			textb.Text = func
			ellipseGrid.Children.Add(textb)
			ellipseGrid.SetRow(textb,0) 
			varsName = TextBlock()
			varsName.FontSize = 9
			varsName.Text = vars
			varsName.HorizontalAlignment = HorizontalAlignment.Right
			ellipseGrid.Children.Add(varsName)
			ellipseGrid.SetRow(varsName,2)
			pass
		textblock.HorizontalAlignment = HorizontalAlignment().Center
		textblock.VerticalAlignment = VerticalAlignment().Center
		ellipseGrid.Children.Add(textblock)
		ellipseGrid.SetRow(textblock,1)

		self.totalEllipses += 1
		return ellipseGrid

	totalEllipses = 0
	def CreateEllipse(self, sender, e):
		dlg = EllipsePrompt()
		dlg.Owner = Window.GetWindow(self)
		result = dlg.ShowDialog()
		writeText = ""
		if result:
			ellipseGrid = self.CreateEllipseShape(dlg.funcNameText.Text,dlg.sendVariables.Text,dlg.radioEnd.IsChecked)
		
			if not dlg.radioEnd.IsChecked:
				self.writeCodeToFileText("def {}({}):".format(dlg.funcNameText.Text,dlg.sendVariables.Text))
				self.isUnderFunc = True
			else:
				self.isUnderFunc = False
			self.addNewRowObject(ellipseGrid)
			pass
		else:
			self.writeDBugText( "Ellipse Prompt was Canceled.\n")
		pass #End of definition CreateEllipse

	def ellipseButton(self,sender,e):
		tb = TextBlock()
		tbFlow = TextBlock()
		arrowBack = Line()
		arrowFront = Line()

		dlg = EllipsePrompt()
		for i in sender.Children:
			if i.Name == "tb":
				tb = i
			elif i.Name == "flowtb":
				tbFlow = i
			elif i.Name == "infront":
				arrowFront = i
			elif i.Name == "inback":
				arrowBack = i
		if tb.Text == "Start":
			dlg.radioStart.IsChecked = True
			dlg.funcNameText.Text = tbFlow.Text
		elif tb.Text == "End":
			dlg.radioEnd.IsChecked = False

		result = dlg.ShowDialog()
		if result:
			if dlg.radioStart.IsChecked:
				tb.Text = "Start"
				#Check if the func name exists already
				if tbFlow.Name == "flowtb":
					tbFlow.Text = dlg.funcNameText.Text
				else:
					tbFlow.Name = "flowtb"
					tbFlow.FontSize = 9
					tbFlow.Text = dlg.funcNameText.Text
					sender.Children.Add(tbFlow)
					sender.SetRow(tbFlow,0)
				sender.Children.Remove(arrowFront)
				if arrowBack != "inback":
					arrowBack = self.createEndLine()
					arrowBack.Name = "inback"
					sender.Children.Add(arrowBack)
					sender.SetRow(arrowBack,2)
			elif dlg.radioEnd.IsChecked:
				tb.Text = "End"
				sender.Children.Remove(tbFlow)
				sender.Children.Remove(arrowBack)
				if arrowFront != "infront":
					arrowFront = self.createStartLine()
					arrowFront.Name = "infront"
					sender.Children.Add(arrowFront)
					sender.SetRow(arrowFront,0)
		#TODO: Create Procedure to edit the TextBox text #.
		pass

	totalRects = 0
	def createRectShape(self, text):
		"""Creates a rectangle grid with the list of text as the conditional statements"""
		newRect = Border()
		newRect.MinHeight = 60
		newRect.MinWidth = 100
		newRect.Background = Brushes.WhiteSmoke
		newRect.BorderBrush = Brushes.Black
		newRect.BorderThickness = Thickness(2.0)
		newRect.Name = "Rectangle{}".format(self.totalRects)
		newRect.HorizontalAlignment = HorizontalAlignment().Center
		newRect.VerticalAlignment = VerticalAlignment().Center
		newRect.Padding = Thickness(5)
		
		#create the statement text
		textblock = TextBlock()
		for i in text:
			textblock.Text += "{}".format(i)
		#textblock.Text = "1st Procedure Statement\n2nd Procedure Statement" #This will be the procedural statements which will be bound to a prompt box
		textblock.HorizontalAlignment = HorizontalAlignment().Left
		textblock.VerticalAlignment = VerticalAlignment().Center
		newRect.AddChild(textblock)
		
		#create a single row grid to hold the lines
		#grid = Grid()
		#rowDef = RowDefinition()
		#rowDef.Height = GridLength(1, GridUnitType.Auto)
		#grid.RowDefinitions.Add(rowDef)
		grid = self.createComponentGrid()
		grid.Children.Add(newRect)
		grid.SetRow(newRect,1)
		
		sArrow = self.createStartLine()
		grid.Children.Add(sArrow)
		grid.SetRow(sArrow, 0)
		eArrow = self.createEndLine()
		grid.Children.Add(eArrow)
		grid.SetRow(eArrow, 2)

		self.totalRects += 1
		return grid

	def CreateRectangle(self, sender, e):
		dlg = RectPrompt()
		dlg.Owner = Window.GetWindow(self)
		result = dlg.ShowDialog()
		if result:
			#Create the acutal rectangle
			grid = self.createRectShape(dlg.returnText)

			for i in dlg.returnText:
				self.writeCodeToFileText(i.strip())
			
			self.addNewRowObject(grid)
			pass
		else:
			self.writeDBugText( "RectPrompt was Canceled")
		pass #End of definition CreateRectangle

	def addArrowstoGrid(self,sender,e):
		#create arrows
		sArrow = self.createStartLine(sender.Children[0].ActualHeight)
		eArrow = self.createEndLine(sender.Children[0].ActualHeight)
		sender.Children.Add(sArrow)
		sender.Children.Add(eArrow)
		pass

	totalPara = 0
	def createParaShape(self, text):
		newPara = Border()
		newPara.MinHeight = 40
		newPara.MinWidth = 100
		newPara.Background = Brushes.Khaki
		newPara.BorderBrush = Brushes.Black
		newPara.BorderThickness = Thickness(2.0)
		newPara.Name = "Parallelogram{}".format(self.totalPara)
		newPara.HorizontalAlignment = HorizontalAlignment().Center
		newPara.VerticalAlignment = VerticalAlignment().Center
		newPara.Padding = Thickness(5)
		newPara.RenderTransform = SkewTransform(-20,0)
		newPara.RenderTransformOrigin = Point(0.5,0.5)
		
		#create the statement text
		textblock = TextBlock()
		textblock.Name = "ioStat"
		textblock.Text = text
		textblock.RenderTransform = SkewTransform(20,0)
		textblock.RenderTransformOrigin = Point(0.5,0.5)
		textblock.HorizontalAlignment = HorizontalAlignment().Left
		textblock.VerticalAlignment = VerticalAlignment().Center
		newPara.AddChild(textblock)
		
		#create grid to organize everything
		grid = self.createComponentGrid()
		grid.Children.Add(newPara)
		grid.SetRow(newPara,1)
		
		sArrow = self.createStartLine()
		grid.Children.Add(sArrow)
		grid.SetRow(sArrow, 0)
		eArrow = self.createEndLine()
		grid.Children.Add(eArrow)
		grid.SetRow(eArrow, 2)

		self.totalPara += 1
		return grid

	def CreatePara(self, sender, e):
		dlg = ParaPrompt()
		dlg.Owner = Window.GetWindow(self)
		result = dlg.ShowDialog()
		if result:
			#Create the acutal rectangle
			grid = self.createParaShape(dlg.tempStore.Text)

			#grid.Loaded += RoutedEventHandler(self.addArrowstoGrid)
			#grid.MouseUp += MouseButtonEventHandler(self.componentButton)

			self.addNewRowObject(grid)

			self.writeCodeToFileText(dlg.tempStore.Text)
			pass
		else:
			self.writeDBugText( "ParaPrompt was Canceled")
		pass #End of definition CreatePara

	def refreshEverything(self, sender, e):
		#This function will allow the for either the flow chart to update from the code
		self.flowView.Children.RemoveRange(0,self.flowView.Children.Count)
		if self.flowView.RowDefinitions.Count > 0:
			self.flowView.RowDefinitions.RemoveRange(0,self.flowView.RowDefinitions.Count)
		self.curGridPosition = [0,0]

		fileText = self.FileText.Text
		dirtyfileTextLines =  fileText.split("\n")
		fileTextLines = []
		for i in dirtyfileTextLines:
			if i.strip() != '':
				fileTextLines.append(i)
		index = 0
		maxIndex = len(fileTextLines) - 1
		while index < len(fileTextLines):
			#try:
			self.writeDBugText("index line {} contains: {}".format(index,fileTextLines[index]))
			if fileTextLines[index] == '':
				index = self.safeIndexAdd(index, maxIndex)
			elif "def " in fileTextLines[index] and "):" in fileTextLines[index] and "\t" not in fileTextLines[index]:
				fileTextLines[index] = fileTextLines[index].strip()
				fileTextLines[index] = fileTextLines[index].split(" ",1)[1]
				fileTextLines[index] = fileTextLines[index].rstrip("):")
				something = fileTextLines[index].split("(",1)
				funcName = something[0]
				varsName = something[1]
				self.addNewRowObject(self.CreateEllipseShape(funcName,varsName,False))
				index = self.safeIndexAdd(index, maxIndex)
				beginIndex = 0 + index
				while(index < len(fileTextLines) and "\t" in fileTextLines[index]):
					index = self.safeIndexAdd(index, maxIndex)
				conditions = []
				while beginIndex < index:
					conditions.append(fileTextLines[beginIndex] + "\n")
					beginIndex += 1
				self.addNewRowObject(self.createRectShape(conditions))
				self.addNewRowObject(self.CreateEllipseShape('','',True))
			elif "if " in fileTextLines[index] and "\t" not in fileTextLines[index]:
				fileTextLines[index] = fileTextLines[index].strip()
				fileTextLines[index] = fileTextLines[index].lstrip("if ")
				fileTextLines[index] = fileTextLines[index].rstrip(":")
				condStatement = fileTextLines[index]
				diamond = self.CreateDiamondShape(condStatement)
				index = self.safeIndexAdd(index, maxIndex)
				beginIndex = 0 + index
				while (index < len(fileTextLines)) and (("\t" in fileTextLines[index]) or ("elif " in fileTextLines[index])): #I DONOT SUPPORT ELIFs or LOOPS because of time constraints
					index = self.safeIndexAdd(index, maxIndex)
				trueConditions = []
				while beginIndex < index:
					trueConditions.append(fileTextLines[beginIndex] + "\n")
					beginIndex += 1
				if "else:" in fileTextLines[index]:
					index = self.safeIndexAdd(index, maxIndex)
					elseIndex = 0 + index
					while (index < len(fileTextLines) and "\t" in fileTextLines[index]):
						index = self.safeIndexAdd(index,maxIndex)
					falseConditions = []
					while elseIndex < index:
						falseConditions.append(fileTextLines[elseIndex] + "\n")
						elseIndex += 1
					self.addNewRowObject(self.CreateDiamondGrid(diamond,trueConditions, falseConditions))
					index = self.safeIndexAdd(index, maxIndex)
				else:
					self.addNewRowObject(self.CreateDiamondGrid(diamond,trueConditions))
					index = self.safeIndexAdd(index, maxIndex)
			elif "#" in fileTextLines[index][0]:
				index = self.safeIndexAdd(index, maxIndex)
			
			else:
				beginIndex = 0 + index
				while (index < len(fileTextLines)) and ("def " not in fileTextLines[index] or "):" not in fileTextLines[index]) and ("if " not in fileTextLines[index]) and (fileTextLines[index] != '') and ("#" not in fileTextLines[index][0]): #IM SENDING IN ALOT OF TRASH
					index = self.safeIndexAdd(index, maxIndex)
				conditions = []
				while beginIndex < index:
					conditions.append(fileTextLines[beginIndex] + "\n")
					beginIndex += 1
				self.addNewRowObject(self.createRectShape(conditions))
				#index = self.safeIndexAdd(index, maxIndex)
			#except:
			#	self.writeDBugText("Something Happened and I don't know what. all i know is the thing didn't refresh on index line {}".format(index))
			#	index = self.safeIndexAdd(index, maxIndex)
			#	pass
		pass #End of defintion refreshEverything

	def safeIndexAdd(self, index, maxIndex):
		returnIndex = index
		if index <= maxIndex:
			returnIndex += 1
		return returnIndex

	def CreateDiamondShape(self, condStatement):
		diaGrid = Grid()
		diaGrid.RowDefinitions.Add(RowDefinition())
		diaGrid.RowDefinitions.Add(RowDefinition())
		diaGrid.ColumnDefinitions.Add(ColumnDefinition())
		diaGrid.ColumnDefinitions.Add(ColumnDefinition())
		diaGrid.ColumnDefinitions.Add(ColumnDefinition())
		diaGrid.ColumnDefinitions.Add(ColumnDefinition())

		# Create This#<Polygon Height="35" Stroke="Black" StrokeThickness="2" Width="85" Points="2,17.5 42.5,2 83,17.5 42.5,33"/>
		diamond = Polygon()
		diamond.Height = 70
		diamond.Width = 170
		diamond.Stroke = Brushes.Black
		diamond.StrokeThickness = 2
		diaPoint = [Point(2,35),Point(85,2),Point(168,35),Point(85,68)]
		diamond.Points = PointCollection(diaPoint)
		diamond.HorizontalAlignment = HorizontalAlignment.Center
		diamond.VerticalAlignment = VerticalAlignment.Center
		diamond.Fill = Brushes.DarkCyan
		diaGrid.Children.Add(diamond)
		diaGrid.SetRow(diamond,0)
		diaGrid.SetRowSpan(diamond, 2)
		diaGrid.SetColumn(diamond,0)
		diaGrid.SetColumnSpan(diamond,4)

		#Create This#<Label Content="Conditional" HorizontalAlignment="Center" Grid.Row="3" VerticalAlignment="Center" IsHitTestVisible="False" Height="33" Width="83" FontSize="10" HorizontalContentAlignment="Center" VerticalContentAlignment="Center" Panel.ZIndex="1"/>
		diaLabel = Label()
		diaLabel.Content = condStatement
		diaLabel.Foreground = Brushes.WhiteSmoke
		diaLabel.HorizontalAlignment = HorizontalAlignment.Center
		diaLabel.VerticalAlignment = VerticalAlignment.Center
		diaLabel.Height = 68
		diaLabel.FontSize = 10
		diaLabel.HorizontalContentAlignment = HorizontalAlignment.Center
		diaLabel.VerticalContentAlignment = VerticalAlignment.Center
		Panel.SetZIndex(diaLabel,1)
		diaGrid.Children.Add(diaLabel)
		diaGrid.SetRow(diaLabel,0)
		diaGrid.SetRowSpan(diaLabel,2)
		diaGrid.SetColumn(diaLabel,0)
		diaGrid.SetColumnSpan(diaLabel,4)

		#Create a True Label to identify which side is which
		trueLabel = Label()
		trueLabel.Content = "True"
		trueLabel.HorizontalAlignment = HorizontalAlignment.Center
		trueLabel.VerticalAlignment = VerticalAlignment.Center
		trueLabel.IsEnabled = False
		diaGrid.Children.Add(trueLabel)
		diaGrid.SetRowSpan(trueLabel,2)

		#Create a False Label to identify which side is which
		falseLabel = Label()
		falseLabel.Content = "False"
		falseLabel.HorizontalAlignment = HorizontalAlignment.Center
		falseLabel.VerticalAlignment = VerticalAlignment.Center
		falseLabel.IsEnabled = False
		diaGrid.Children.Add(falseLabel)
		diaGrid.SetRowSpan(falseLabel,2)
		diaGrid.SetColumn(falseLabel,3)

		#Create a Line to connect the diamond to the later components
		connect = Line()
		connect.X1 = 1
		connect.Stretch = Stretch.Fill
		connect.VerticalAlignment = VerticalAlignment.Center
		connect.HorizontalAlignment = HorizontalAlignment.Stretch
		connect.StrokeEndLineCap = PenLineCap.Square
		connect.StrokeStartLineCap = PenLineCap.Square
		connect.Stroke = Brushes.Black
		connect.StrokeThickness = 10
		Panel.SetZIndex(connect,-1)
		diaGrid.Children.Add(connect)
		diaGrid.SetRow(connect, 0)
		diaGrid.SetRowSpan(connect, 2)
		diaGrid.SetColumn(connect, 1)
		diaGrid.SetColumnSpan(connect, 2)

		#Connect the connect line to the bottom of the grid on the Left side
		leftLine = Line()
		leftLine.Y2 = 1
		leftLine.Stretch = Stretch.Fill
		leftLine.VerticalAlignment = VerticalAlignment.Stretch
		leftLine.HorizontalAlignment = HorizontalAlignment.Center
		leftLine.StrokeEndLineCap = PenLineCap.Square
		leftLine.StrokeStartLineCap = PenLineCap.Round
		leftLine.Stroke = Brushes.Black
		leftLine.StrokeThickness = 10
		diaGrid.Children.Add(leftLine)
		diaGrid.SetRow(leftLine,1)
		diaGrid.SetColumn(leftLine,0)
		diaGrid.SetColumnSpan(leftLine,2)
		#Connect the connect line to the bottom of the grid on the right side
		rightLine = Line()
		rightLine.Y2 = 1
		rightLine.Stretch = Stretch.Fill
		rightLine.VerticalAlignment = VerticalAlignment.Stretch
		rightLine.HorizontalAlignment = HorizontalAlignment.Center
		rightLine.StrokeEndLineCap = PenLineCap.Square
		rightLine.StrokeStartLineCap = PenLineCap.Round
		rightLine.Stroke = Brushes.Black
		rightLine.StrokeThickness = 10
		diaGrid.Children.Add(rightLine)
		diaGrid.SetRow(rightLine,1)
		diaGrid.SetColumn(rightLine,2)
		diaGrid.SetColumnSpan(rightLine,2)

		return diaGrid

	def CreateDiamondGrid(self, diamond , trueText, elseText = []):
		tempDiaGrid = Grid()
		tempDiaGrid.ColumnDefinitions.Add(ColumnDefinition())
		tempDiaGrid.ColumnDefinitions.Add(ColumnDefinition())
		tempDiaGrid.RowDefinitions.Add(RowDefinition())
		tempDiaGrid.RowDefinitions.Add(RowDefinition())
		tempDiaGrid.RowDefinitions.Add(RowDefinition())
		tempDiaGrid.RowDefinitions.Add(RowDefinition())
		tempDiaGrid.RowDefinitions.Add(RowDefinition())

		#add the diamond grid to the return tempgrid
		tempDiaGrid.Children.Add(diamond)
		tempDiaGrid.SetRow(diamond, 1)
		tempDiaGrid.SetColumn(diamond,0)
		tempDiaGrid.SetColumnSpan(diamond,2)

		sArrow = self.createStartLine()
		tempDiaGrid.Children.Add(sArrow)
		tempDiaGrid.SetRow(sArrow,0)
		tempDiaGrid.SetColumnSpan(sArrow, 2)

		eArrow = self.createEndLine()
		tempDiaGrid.Children.Add(eArrow)
		tempDiaGrid.SetRow(eArrow,4)
		tempDiaGrid.SetColumnSpan(eArrow, 2)

		trueCol = self.createRectShape(trueText)
		tempDiaGrid.Children.Add(trueCol)
		tempDiaGrid.SetRow(trueCol,2)
		tempDiaGrid.SetColumn(trueCol,0)

		if len(elseText) > 0:
			elseCol = self.createRectShape(elseText)
			tempDiaGrid.Children.Add(elseCol)
			tempDiaGrid.SetRow(elseCol,2)
			tempDiaGrid.SetColumn(elseCol,1)
		else:
			#create a straight line
			srtLine = Line()
			srtLine.Y1 = 1
			srtLine.HorizontalAlignment = HorizontalAlignment.Center
			srtLine.VerticalAlignment = VerticalAlignment.Stretch
			srtLine.Stroke = Brushes.Black
			srtLine.StrokeThickness = 10
			srtLine.Stretch = Stretch.Fill
			srtLine.StrokeEndLineCap = PenLineCap.Square
			srtLine.StrokeStartLineCap = PenLineCap.Square
			tempDiaGrid.Children.Add(srtLine)
			tempDiaGrid.SetColumn(srtLine, 1)
			tempDiaGrid.SetRow(srtLine, 2)
			pass

		lastGrid = Grid()
		lastGrid.RowDefinitions.Add(RowDefinition())
		lastGrid.RowDefinitions.Add(RowDefinition())
		lastGrid.ColumnDefinitions.Add(ColumnDefinition())
		lastGrid.ColumnDefinitions.Add(ColumnDefinition())
		lastGrid.ColumnDefinitions.Add(ColumnDefinition())
		lastGrid.ColumnDefinitions.Add(ColumnDefinition())

		lconnect = Line()
		lconnect.X1 = 1
		lconnect.Stretch = Stretch.Fill
		lconnect.VerticalAlignment = VerticalAlignment.Center
		lconnect.HorizontalAlignment = HorizontalAlignment.Stretch
		lconnect.StrokeEndLineCap = PenLineCap.Square
		lconnect.StrokeStartLineCap = PenLineCap.Square
		lconnect.Stroke = Brushes.Black
		lconnect.StrokeThickness = 10
		Panel.SetZIndex(lconnect,-1)
		lastGrid.Children.Add(lconnect)
		lastGrid.SetRow(lconnect, 1)
		lastGrid.SetColumn(lconnect,1)
		lastGrid.SetColumnSpan(lconnect,2)

		eleftLine = Line()
		eleftLine.Y2 = 1
		eleftLine.Stretch = Stretch.Fill
		eleftLine.VerticalAlignment = VerticalAlignment.Stretch
		eleftLine.HorizontalAlignment = HorizontalAlignment.Center
		eleftLine.StrokeEndLineCap = PenLineCap.Round
		eleftLine.StrokeStartLineCap = PenLineCap.Square
		eleftLine.Stroke = Brushes.Black
		eleftLine.StrokeThickness = 10
		lastGrid.Children.Add(eleftLine)
		lastGrid.SetRowSpan(eleftLine,2)
		lastGrid.SetColumnSpan(eleftLine,2)

		erightLine = Line()
		erightLine.Y2 = 1
		erightLine.Stretch = Stretch.Fill
		erightLine.VerticalAlignment = VerticalAlignment.Stretch
		erightLine.HorizontalAlignment = HorizontalAlignment.Center
		erightLine.StrokeEndLineCap = PenLineCap.Round
		erightLine.StrokeStartLineCap = PenLineCap.Square
		erightLine.Stroke = Brushes.Black
		erightLine.StrokeThickness = 10
		lastGrid.Children.Add(erightLine)
		lastGrid.SetRowSpan(erightLine,2)
		lastGrid.SetColumn(erightLine,2)
		lastGrid.SetColumnSpan(erightLine,2)


		tempDiaGrid.Children.Add(lastGrid)
		tempDiaGrid.SetRow(lastGrid, 3)
		tempDiaGrid.SetColumnSpan(lastGrid,2)

		return tempDiaGrid

	def CreateDiamond(self, sender, e):
		dlg = ConPrompt()
		dlg.Owner = Window.GetWindow(self)
		result = dlg.ShowDialog()
		if result:
			tempGridCopy = Grid()
			tempGridCopy = self.deepCopyElement(dlg.tempGrid)
			sArrow = self.createStartLine()
			tempGridCopy.Children.Add(sArrow)
			tempGridCopy.SetRow(sArrow,0)
			tempGridCopy.SetColumnSpan(sArrow, 2)
			eArrow = self.createEndLine()
			tempGridCopy.Children.Add(eArrow)
			tempGridCopy.SetRow(eArrow,4)
			tempGridCopy.SetColumnSpan(eArrow, 2)
			tempGridCopy.Visibility = Visibility.Visible
			self.addNewRowObject(tempGridCopy)
			self.writeCodeToFileText(dlg.tempText.Text)
		pass

	def openAboutWindow(self, sender, e):
		about = AboutWindow()
		about.Owner = Window.GetWindow(self)
		result = about.ShowDialog()
		text = about.visitMe.Text
		self.writeDBugText( "The help window just closed. Here's proof:\n\t{}".format(text))
		pass

	def openFile(self, sender, e):
		file = OpenFileDialog()
		file.DefaultExt = "py"
		file.Filter = "Python documents|*.py"
		result = file.ShowDialog()

		if result:
			self.OpenFile = file.FileName
			self.writeFiletoFileText()
			self.refreshEverything(sender, e)
		pass

	def writeFiletoFileText(self):
		pyFile = open(self.OpenFile,"r")
		self.FileText.Text = ''
		for line in pyFile:
			self.FileText.Text += line
		pyFile.close()
		pass

	def saveFileAs(self, sender, e):
		file = SaveFileDialog()
		file.DefaultExt = "py"
		file.Filter = "Python documents|*.py"
		file.AddExtension = True
		file.InitialDirectory = self.OpenFile
		file.OverwritePrompt = True
		file.CheckPathExists = True
		file.CreatePrompt = True

		result = file.ShowDialog()
		if result:
			self.OpenFile = file.FileName
			self.writeFileTexttoFile()
		pass

	def writeFileTexttoFile(self):
		pyFile = open("C:\Users\Zovin\Desktop\Test.py","w+")
		pyFile.write(self.FileText.Text)
		pyFile.close()
		pass
	
	def writeCodeToFileText(self,writeMe):
		if(self.isUnderFunc):
			self.FileText.Text += "\t"
		self.FileText.Text += "{}\n".format(writeMe)
		pass

	def writeDBugText(self,write):
		if(DEBUG):
			self.dbugWin.dbugTxt.Text += ("{}\n".format(write))
			pass
		pass

	def deepCopyElement(self, element): #Source: http://blogs.msdn.com/b/mikehillberg/archive/2007/05/01/clonewithxamlwriterxamlreader.aspx
		xaml = Markup.XamlWriter.Save(element) #Saves xaml object as a string
		deepCopiedElement = Markup.XamlReader.Load(XmlTextReader(StringReader(xaml)))
		deepCopiedElement.Name = ""
		return deepCopiedElement

	def saveFile(self, sender, e):
		if len(self.OpenFile) > 0:
			self.writeFileTexttoFile()
		else:
			self.saveFileAs(sender, e)
		pass

	def newFile(self,sender,e):
		self.flowView.Children.RemoveRange(0,self.flowView.Children.Count)
		if self.flowView.RowDefinitions.Count > 0:
			self.flowView.RowDefinitions.RemoveRange(0,self.flowView.RowDefinitions.Count)
		self.curGridPosition = [0,0]
		self.OpenFile = ''
		self.FileText.Text = ''
		pass

	def exit(self, sender,e):
		Application.Shutdown(me)
		pass

	def openTutorial(self, sender, e):
		pass
	pass#end of class
if __name__ == '__main__':
    me.Run(MyWindow())