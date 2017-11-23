import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaFX as OpenMayaFX

command_name = 'vertexParticle'

kHelpFlag = '-h'
kHelpLongFlag = '-help'
kSparseFlag = '-s'
kSparseLongFlag = '-sparse'
helpMessage = 'This command is used to attach a particle on each vertext of a mesh'

class VertexParticleCommand(OpenMayaMPx.MPxCommand):

	sparse = None
	def __init__(self):
		"""
		use the parent __init__
		"""
		OpenMayaMPx.MPxCommand.__init__(self)
		
	def doIt(self, args):
		print 'doIt...'
		self.parseArguments(args)
		
		if self.sparse != None:
			self.redoIt()
		
		return
				
	def redoIt(self):
		m_sel = OpenMaya.MSelectionList()
		dag_path = OpenMaya.MDagPath()
		fn_mesh = OpenMaya.MFnMesh()
		
		OpenMaya.MGlobal.getActiveSelectionList(m_sel)
		if m_sel.length() >= 1:
			try:
				m_sel.getDagPath(0, dag_path)
				fn_mesh.setObject(dag_path)
			except:
				print 'Please select a poly mesh.'
				return
		else:
			print 'Please select a poly mesh.'
			return
			
		point_array = OpenMaya.MPointArray()
		fn_mesh.getPoints(point_array, OpenMaya.MSpace.kWorld)
		
		# create a particle system
		fn_particle = OpenMayaFX.MFnParticleSystem()
		self.mobj_particle = fn_particle.create()
		
		# this is a Maya bug
		fn_particle = OpenMayaFX.MFnParticleSystem(self.mobj_particle)
		
		counter = 0
		for i in xrange(point_array.length()):
			if i % self.sparse == 0:
				fn_particle.emit(point_array[i])
				counter += 1
		
		print 'Total points: %d' % counter
		fn_particle.saveInitialState()
		
		return
		
	def parseArguments(self, args):
		m_syntax = self.syntax()
		
		try:
			parsed_args = OpenMaya.MArgDatabase(m_syntax, args)
		except:
			print 'Incorrect Argument!'
			return
		
		# sparse flag
		if parsed_args.isFlagSet(kSparseFlag):
			self.sparse = parsed_args.flagArgumentDouble(kSparseFlag, 0)
		if parsed_args.isFlagSet(kSparseLongFlag):
			self.sparse = parsed_args.flagArgumentDouble(kSparseLongFlag, 0)
		
		# help flag
		if parsed_args.isFlagSet(kHelpFlag):
			self.setResult(helpMessage)
			return
		if parsed_args.isFlagSet(kHelpLongFlag):
			self.setResult(helpMessage)
			return   
			
def cmd_creator():
	return OpenMayaMPx.asMPxPtr(VertexParticleCommand())
	
def syntax_creator():
	syntax = OpenMaya.MSyntax()
	syntax.addFlag(kHelpFlag, kHelpLongFlag)
	syntax.addFlag(kSparseFlag, kSparseLongFlag, OpenMaya.MSyntax.kDouble)
	
	return syntax
		
def initializePlugin(mObject):
	mplugin = OpenMayaMPx.MFnPlugin(mObject)
	
	try:
		mplugin.registerCommand(command_name, cmd_creator, syntax_creator)
	except:
		sys.stderr.write('Failed to register: %s' % command_name)
		
def uninitializePlugin(mObject):
	mplugin = OpenMayaMPx.MFnPlugin(mObject)
	
	try:
		mplugin.deregisterCommand(command_name)
	except:
		sys.stderr.write('Failed to de-register: %s' % command_name)
