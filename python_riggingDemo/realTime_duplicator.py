from PySide import QtCore, QtGui

class RealTimeDuplicator(QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(RealTimeDuplicator, self).__init__(parent)
        
        self.setWindowTitle('Real Time Duplicator')
        
        mainLayout = QtGui.QVBoxLayout()
        self.setLayout(mainLayout)
        
        translateLabel = QtGui.QLabel('Translate')
        translateHBox = QtGui.QHBoxLayout()
        self.transXSpin = QtGui.QDoubleSpinBox()
        self.transYSpin = QtGui.QDoubleSpinBox()
        self.transZSpin = QtGui.QDoubleSpinBox()
        
        rotateLabel = QtGui.QLabel('Rotate')
        rotateHBox = QtGui.QHBoxLayout()
        self.rotXSpin = QtGui.QDoubleSpinBox()
        self.rotYSpin = QtGui.QDoubleSpinBox()
        self.rotZSpin = QtGui.QDoubleSpinBox()
        
        scaleLabel = QtGui.QLabel('Scale')
        scaleHBox = QtGui.QHBoxLayout()
        self.scaleXSpin = QtGui.QDoubleSpinBox()
        self.scaleYSpin = QtGui.QDoubleSpinBox()
        self.scaleZSpin = QtGui.QDoubleSpinBox()
        
        self.testSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.testSlider.valueChanged.connect(self.sliderChange)

        mainLayout.addWidget(translateLabel)
        mainLayout.addLayout(translateHBox)
        translateHBox.addWidget(self.transXSpin)
        translateHBox.addWidget(self.transYSpin)
        translateHBox.addWidget(self.transZSpin)
        
        mainLayout.addWidget(rotateLabel)
        mainLayout.addLayout(rotateHBox)
        rotateHBox.addWidget(self.rotXSpin)
        rotateHBox.addWidget(self.rotYSpin)
        rotateHBox.addWidget(self.rotZSpin)
        
        mainLayout.addWidget(scaleLabel)
        mainLayout.addLayout(scaleHBox)
        scaleHBox.addWidget(self.scaleXSpin)
        scaleHBox.addWidget(self.scaleYSpin)
        scaleHBox.addWidget(self.scaleZSpin)
        
        
        mainLayout.addWidget(self.testSlider)
        
        self.orig = mc.ls(sl=True)
        self.dupes = list()
        
    def sliderChange(self):
        num_dupes = self.testSlider.value()
        if self.dupes:
            mc.delete(self.dupes)
            self.dupes = list()
        
        trans_x = self.transXSpin.value()
        trans_y = self.transYSpin.value()
        trans_z = self.transZSpin.value()
        
        rot_x = self.rotXSpin.value()
        rot_y = self.rotYSpin.value()
        rot_z = self.rotZSpin.value()
        
        scale_x = self.scaleXSpin.value()
        scale_y = self.scaleYSpin.value()
        scale_z = self.scaleZSpin.value()
        
        
        for idx in xrange(num_dupes):
            current_dupes = mc.duplicate(self.orig)
            move_amount = [x * (idx+1) for x in [trans_x, trans_y, trans_z]]
            rotate_amount = [x * (idx+1) for x in [rot_x, rot_y, rot_z]]
            scale_amount = [x for x in [scale_x, scale_y, scale_z]]

            mc.move(move_amount[0], move_amount[1], move_amount[2], current_dupes, relative=True)
            mc.rotate(rotate_amount[0], rotate_amount[1], rotate_amount[2], current_dupes, relative=True)
            mc.scale(scale_amount[0], scale_amount[1], scale_amount[2], current_dupes, relative=True)

            self.dupes.extend(current_dupes)
        
		
def main():
	test_ui = RealTimeDuplicator()
	test_ui.show()
	
	
main()