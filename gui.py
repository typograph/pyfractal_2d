from PySide import QtGui
from PySide.QtCore import Qt

class ColorSelect(QtGui.QFrame):

	def __init__(self, color, parent=None):
		QtGui.QFrame.__init__(self, parent)

		self.custom_palette = QtGui.QPalette(self.palette())
		self.setAutoFillBackground(True)
		
		self.setMinimumSize(20,20)
		sp = QtGui.QSizePolicy(
				QtGui.QSizePolicy.Expanding,
				QtGui.QSizePolicy.Expanding)
		sp.setHeightForWidth(True)
		self.setSizePolicy(sp)
		
		self.set_color(color)

	def set_color(self,color):
		self.color = color
		self.custom_palette.setColor(QtGui.QPalette.Window, color)
		self.setPalette(self.custom_palette)

	def heightForWidth(self, w):
		return w

class FractalColor(QtGui.QFrame):
	
	def __init__(self, color, parent = None):
		QtGui.QFrame.__init__(self, parent)

		self.setFrameShape(QtGui.QFrame.Panel)
	
		layout = QtGui.QGridLayout(self)
		
		self.selfcolor = ColorSelect(color, self)
		layout.addWidget(self.selfcolor,0,0)
		
		self.wspin = QtGui.QSpinBox(self)
		self.wspin.setRange(1,10)
		self.wspin.setValue(3)
		self.wspin.valueChanged.connect(self.update_grid_dim)
		layout.addWidget(self.wspin,1,0)
		
		self.hspin = QtGui.QSpinBox(self)
		self.hspin.setRange(1,10)
		self.hspin.setValue(3)
		self.hspin.valueChanged.connect(self.update_grid_dim)
		layout.addWidget(self.hspin,2,0)
		
		self.grid = QtGui.QWidget(self)
		self.grid.setLayout(QtGui.QGridLayout())
		self.gW, self.gH = 0,0
		self.set_grid_dim(3,3)
		layout.addWidget(self.grid,0,1,3,1)
			
	def update_grid_dim(self):
		self.set_grid_dim(self.wspin.value(), self.hspin.value())
		
	def set_grid_dim(self,W,H):
		for col in range(self.gW, W):
			for row in range(self.gH):
				self.grid.layout().addWidget(ColorSelect(Qt.white,self.grid), row, col)
		for row in range(self.gH, H):
			for col in range(W):
				self.grid.layout().addWidget(ColorSelect(Qt.white,self.grid), row, col)
			
		self.gW, self.gH = W, H
		
class MainWin(QtGui.QFrame):
	def __init__(self):
		QtGui.QFrame.__init__(self)
		
		self.setLayout(QtGui.QHBoxLayout())
		
		self.imgLabel = QtGui.QLabel(self)
		self.imgLabel.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		self.layout().addWidget(self.imgLabel)
		
		self.colors = QtGui.QFrame(self)
		self.colors.setFrameShape(QtGui.QFrame.Panel)
		self.layout().addWidget(self.colors)
		
		self.colors.setLayout(QtGui.QVBoxLayout())
		self.colors.layout().addWidget(FractalColor(Qt.white,self.colors))
		
		self.plusbtn = QtGui.QPushButton("+",self.colors)
		self.colors.layout().addWidget(self.plusbtn)
		
		self.colors.layout().addStretch(1)
		
	def addColor(self,color):
		
		self.colors.layout().insertWidget(self.colors.layout().count() - 2, FractalColor(color,self.colors))
		
if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	mainw = MainWin()
	mainw.show()
	mainw.addColor(Qt.black)
	app.exec_()

