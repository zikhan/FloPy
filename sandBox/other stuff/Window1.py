import wpf
import clr
clr.AddReference("windowsbase")

from System.Windows import (Application, Window, Thickness, HorizontalAlignment, SizeToContent, CornerRadius, Point)
from System.Windows.Controls import (Grid, ColumnDefinition, RowDefinition, Label, Border, ToolTip)
from System.Windows.Media import (Brushes, Colors, GradientStop, LinearGradientBrush)
from System.Windows.Input import Cursors


class ControlsExample(Window):
	def __init__(self):
		#wpf.LoadComponent(self,'Window1.xaml')
		grid = self.getGrid()
		grid.Background = GetLinearGradientBrush()
		self.createControls(grid)

		border = Border()
		border.BorderThickness = Thickness(5)
		border.CornerRadius = CornerRadius(10)
		border.BorderBrush = Brushes.Blue
		border.Background = Brushes.Yellow
		border.Padding = Thickness(5)
		border.Child = grid
		self.Content = border

		self.Title = 'WPF Controls Example'
		self.SizeToContent = SizeToContent.Height
		self.Width = 800

	def getGrid(self):
		grid = Grid()
		grid.showGridLines = True
		# 3x3 grid
		for i in range(3):
			grid.ColumnDefinitions.Add(ColumnDefinition())
			grid.RowDefinitions.Add(RowDefinition())

		label = Label()
		label.Margin = Thickness(15)
		label.FontSize = 16
		label.Content = "Nothing Yet..."
		label.HorizontalAlignment = HorizontalAlignment.Center
		self.label = label

		grid.SetColumnSpan(self.label,3)
		grid.SetRow(self.label,0)
		grid.Children.Add(self.label)

		return grid

	#Helper Functions
	def GetLinearGradientBrush():
		brush = LinearGradientBrush()
		brush.StartPoint = Point(0,0)
		brush.EndPoint = Point(1,1)
		stops = [
			(Colors.Yellow, 0.0),
			(Colors.Tomato, 0.25),
			(Colors.DeepSkyBlue, 0.75),
			(Colors.LimeGreen, 1.0)
		]
		for color, stop in stops:
			brush.GradientStops.Add(GradientStop(color,stop))
		return brush
	
	def SetGridChild(grid, child, col, row, tooltip):
		if hasattr(child, 'FontSize'):
			child.FontSize = 16
		child.Margin = Thickness(15)
		child.Cursor = Cursors.Hand
		child.ToolTip = ToolTip(Content=tooltip)
		grid.SetRow(child, row)
		grid.Children.Add(child)