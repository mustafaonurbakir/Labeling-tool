from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import time

class Cluster(QObject):
	def __init__(self):
		QObject.__init__(self)
        
	kphResult = pyqtSignal(int, arguments=['kph'])
	powerResult = pyqtSignal(int, arguments=['power'])

	# Slot for summing two numbers
	@pyqtSlot()
	def kph(self):
		self.kphResult.emit(100)
	
	# Slot for subtraction of two numbers
	@pyqtSlot()
	def power(self):
		self.powerResult.emit(10)
 

if __name__ == "__main__":
	import sys

	# Create an instance of the application
	app = QGuiApplication(sys.argv)
	# Create QML engine
	engine = QQmlApplicationEngine()
	
	cluster = Cluster()
	# And register it in the context of QML
	engine.rootContext().setContextProperty("cluster", cluster)
	
	try:
		engine.load("cluster/qml/Cluster.qml")
		engine.quit.connect(app.quit)
		sys.exit(app.exec_())
	except:
		pass
	
	
	
	
	
	
	



    
    
