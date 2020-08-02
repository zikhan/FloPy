import clr
clr.AddReference('IronPython.Wpf')

import wpf

from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Shapes import *
from System.Windows.Media import *
from Microsoft.Win32 import *
from System.Windows.Input import *

from ParaPrompt import *
from RectPrompt import *

class ConPrompt(Window):
	statStore_T = []
	statStore_F = []
	isElse = True

	def __init__(self):
		wpf.LoadComponent(self, 'ConPrompt.xaml')
		self.statStore_T = []
		self.statStore_F = []
		pass

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

	def createComponentGrid(self):	
		newGrid = Grid()
		newGrid.RowDefinitions.Add(RowDefinition()) #Row for Flow Name
		newGrid.RowDefinitions.Add(RowDefinition()) #Row for actual flow component
		newGrid.RowDefinitions.Add(RowDefinition()) #Row for variables affected

		return newGrid

	curGridPosition = [0,0]
	def addNewRowObject_T(self, RowObject):
		rowDef = RowDefinition()
		rowDef.Height = GridLength(1,GridUnitType.Auto)
		rowDef.MinHeight = 80
		self.trueGrid.RowDefinitions.Add(rowDef)
		self.trueGrid.Children.Add(RowObject)
		#self.flowView.SetRow(RowObject,self.flowView.Children.IndexOf(RowObject))

		self.trueGrid.SetRow(RowObject,self.curGridPosition[0])
		self.curGridPosition[0] += 1
		pass

	curGridPosition_F = [0,0]
	def addNewRowObject_F(self, RowObject):
		rowDef = RowDefinition()
		rowDef.Height = GridLength(1,GridUnitType.Auto)
		rowDef.MinHeight = 80
		self.falseGrid.RowDefinitions.Add(rowDef)
		self.falseGrid.Children.Add(RowObject)
		#self.flowView.SetRow(RowObject,self.flowView.Children.IndexOf(RowObject))

		self.falseGrid.SetRow(RowObject,self.curGridPosition_F[0])
		self.curGridPosition_F[0] += 1
		pass

	totalRects = 0
	def CreateRectangle(self, sender, e):
		who = 1 if "True" in sender.Name else 0
		who = 0 if "False" in sender.Name else 1

		dlg = RectPrompt()
		result = dlg.ShowDialog()
		if result:
			#Create the acutal rectangle
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
			returnedText = []
			returnedText = dlg.returnText
			for i in returnedText:
				textblock.Text += "{}".format(i)
				if who:
					self.statStore_T.append(i)
				elif not who:
					self.statStore_F.append(i)
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

			#grid.Loaded += RoutedEventHandler(self.addArrowstoGrid)
			#grid.MouseUp += MouseButtonEventHandler(self.componentButton)

			#self.addNewRowObject(grid)
			if who:
				self.addNewRowObject_T(grid)
			elif not who:
				self.addNewRowObject_F(grid)
			self.totalRects += 1

		pass #End of definition CreateRectangle

	totalPara = 0
	def CreatePara(self, sender, e):
		who = 1 if "True" in sender.Name else 0
		who = 0 if "False" in sender.Name else 1
		
		dlg = ParaPrompt()
		result = dlg.ShowDialog()
		if result:
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
			textblock.Text = dlg.tempStore.Text
			if who:
				self.statStore_T.append(dlg.tempStore.Text)
			elif not who:
				self.statStore_F.append(dlg.tempStore.Text)
			textblock.RenderTransform = SkewTransform(20,0)
			textblock.RenderTransformOrigin = Point(0.5,0.5)
			textblock.HorizontalAlignment = HorizontalAlignment().Left
			textblock.VerticalAlignment = VerticalAlignment().Center
			newPara.AddChild(textblock)

			#create a single row grid to hold the lines
			#grid = Grid()
			#rowDef = RowDefinition()
			#rowDef.Height = GridLength(1, GridUnitType.Auto)
			#grid.RowDefinitions.Add(rowDef)
			grid = self.createComponentGrid()
			grid.Children.Add(newPara)
			grid.SetRow(newPara,1)
		
			sArrow = self.createStartLine()
			grid.Children.Add(sArrow)
			grid.SetRow(sArrow, 0)
			eArrow = self.createEndLine()
			grid.Children.Add(eArrow)
			grid.SetRow(eArrow, 2)

			#grid.Loaded += RoutedEventHandler(self.addArrowstoGrid)
			#grid.MouseUp += MouseButtonEventHandler(self.componentButton)

			#self.addNewRowObject(grid)
			if who:
				self.addNewRowObject_T(grid)
			elif not who:
				self.addNewRowObject_F(grid)
			self.totalPara += 1

		pass

	def buttonOk_click(self, sender, e):
		#Create a Grid for the Diamond
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
		diaLabel.Content = self.condStatement.Text
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
		connect.StrokeEndLineCap = PenLineCap.Round
		connect.StrokeStartLineCap = PenLineCap.Round
		connect.Stroke = Brushes.Black
		connect.StrokeThickness = 10
		Panel.SetZIndex(connect,-1)
		diaGrid.Children.Add(connect)
		diaGrid.SetRow(connect, 0)
		diaGrid.SetRowSpan(connect,2)
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

		#add the diamond grid to the return tempgrid
		self.tempGrid.Children.Add(diaGrid)
		self.tempGrid.SetRow(diaGrid, 1)
		self.tempGrid.SetColumn(diaGrid,0)
		self.tempGrid.SetColumnSpan(diaGrid,2)

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


		self.tempGrid.Children.Add(lastGrid)
		self.tempGrid.SetRow(lastGrid, 3)
		self.tempGrid.SetColumnSpan(lastGrid,2)

		#add the user created true grid to the return tempgrid
		parent = self.trueGrid.Parent
		parent.Content = Grid()
		self.trueGrid.Background = None
		self.tempGrid.Children.Add(self.trueGrid)
		self.tempGrid.SetColumn(self.trueGrid, 0)
		self.tempGrid.SetRow(self.trueGrid, 2)
		self.tempText.Text = "if " + self.condStatement.Text + " :\n"
		for i in self.statStore_T:
			self.tempText.Text += "\t" + i + "\n"
			pass

		if self.elseYes.IsChecked:
			#add the user created false grid to the return tempgrid
			parent = self.falseGrid.Parent
			parent.Content = Grid()
			self.falseGrid.Background = None
			self.tempGrid.Children.Add(self.falseGrid)
			self.tempGrid.SetColumn(self.falseGrid, 1)
			self.tempGrid.SetRow(self.falseGrid, 2)
			self.tempText.Text += "else:\n"
			for i in self.statStore_F:
				self.tempText.Text += "\t" + i + "\n"
				pass
			pass
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
			self.tempGrid.Children.Add(srtLine)
			self.tempGrid.SetColumn(srtLine, 1)
			self.tempGrid.SetRow(srtLine, 2)
			pass
		self.DialogResult = True
		pass

	def noChkd(self, sender, e):
		self.falseScroll.IsEnabled = False
		self.paraFalseButton.IsEnabled = False
		self.rectFalseButton.IsEnabled = False
		self.falseGrid.Background = Brushes.Gray
		self.isElse = False
		pass

	def yesChked(self, sender, e):
		self.falseScroll.IsEnabled = True
		self.paraFalseButton.IsEnabled = True
		self.rectFalseButton.IsEnabled = True
		self.falseGrid.Background = self.falseGridBKGD
		self.isElse = True
		pass

	def window_opened(self, sender, e):
		self.falseGridBKGD = self.falseGrid.Background
		self.statStore_F = []
		self.statStore_T = []
		pass
