from PyQt5 import QtCore, QtGui, QtWidgets
import sys
class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(400, 300)
		self.pushButton = QtWidgets.QPushButton(Form)
		self.pushButton.setGeometry(QtCore.QRect(150, 200, 100, 75))
		self.pushButton.setObjectName("pushButton")
		self.label = QtWidgets.QLabel(Form)
		self.label.setGeometry(QtCore.QRect(170, 110, 50, 12))
		self.label.setObjectName("label")
		self.retranslateUi(Form)
		
		self.pushButton.clicked.connect(Form.button_click)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Form"))
		self.pushButton.setText(_translate("Form", "flag_change"))
		self.label.setText(_translate("Form","close_flag"))

class Test(QtWidgets.QDialog):
	def __init__(self,parent=None):
		super(Test, self).__init__(parent)
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.close_flag = False
	
	def button_click(self): 
		if self.close_flag == False:
			self.close_flag = True
			self.ui.label.setText(str(self.close_flag))

		elif self.close_flag == True:
			self.close_flag = False
			self.ui.label.setText(str(self.close_flag))
	
	def closeEvent(self,event):
		if self.close_flag == True:
			event.accept()
		elif self.close_flag == False:
			event.ignore()

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = Test()
	window.show()
	sys.exit(app.exec_())