# Import Block
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import sys

# Node Registration Info
kAddUtilNodeTypeName = "TwistDispersion"
kAddUtilNodeClassify = "utility/general"
kAddUtilNodeId       = OpenMaya.MTypeId(0x12345)

# Default Values for node attributes

class TwistDispersionNode(OpenMayaMPx.MPxNode):
	"""
	A node that computes twist deispersion based on 
	incoming rotation value divided by number of twist joints
	"""

	imput         = OpenMaya.MObject()
	inputTwist    = OpenMaya.MObject()
	jointNumber   = OpenMaya.MObject()
	negativeTwist = OpenMaya.MObject()
	disperseTwist = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def compute(self, plug, dataBlock):
		if plug == TwistDispersionNode.negativeTwist or TwistDispersionNode.disperseTwist:
		
			# Get Node Input Attributes
			try:
				input_dataHandle1 = dataBlock.inputValue( TwistDispersionNode.inputTwist )
			except:
				sys.stderr.write( "Failed to get MDataHandle inputValue inputTwist" )
				raise
			try:
				input_dataHandle2 = dataBlock.inputValue( TwistDispersionNode.jointNumber )
			except:
				sys.stderr.write( "Failed to get MDataHandle inputValue jointNumber" )
				raise

			# Get Node Output Attributes
			try:
				Output_dataHandle1 = dataBlock.outputValue( TwistDispersionNode.negativeTwist )
			except:
				sys.stderr.write( "Failed to get MDataHandle inputValue negativeTwist" )
				raise
			try:
				Output_dataHandle2 = dataBlock.outputValue( TwistDispersionNode.disperseTwist )
			except:
				sys.stderr.write( "Failed to get MDataHandle inputValue disperseTwist" )
				raise

			inputTwist_value  = input_dataHandle1.asFloat()
			jointNumber_value = input_dataHandle2.asFloat()

			# Compute negative twist
			result1 = (inputTwist_value / (-1))

			# Compute disperse twist
			result2 = (inputTwist_value / jointNumber_value)

			# Set outgoing Plug
			Output_dataHandle1.setFloat(result1)
			Output_dataHandle2.setFloat(result2)

			dataBlock.setClean(plug)

		else:
			return OpenMaya.kUnknownParameter

def nodeCreator():
	return OpenMayaMPx.asMPxPtr( TwistDispersionNode() )

def nodeInitializer():
	nAttr = OpenMaya.MFnNumericAttribute()

	# Initialize input attributes
	TwistDispersionNode.inputTwist = nAttr.create("inputTwist", "inT", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)

	TwistDispersionNode.jointNumber = nAttr.create("jointNumber", "jNum", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)

	# Initialize output attributes
	TwistDispersionNode.negativeTwist = nAttr.create("negativeTwist", "negT", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
		
	TwistDispersionNode.disperseTwist = nAttr.create("disperseTwist", "disT", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)	

	# Add the input and output attributes
	TwistDispersionNode.addAttribute( TwistDispersionNode.inputTwist )
	TwistDispersionNode.addAttribute( TwistDispersionNode.jointNumber )
	TwistDispersionNode.addAttribute( TwistDispersionNode.negativeTwist )
	TwistDispersionNode.addAttribute( TwistDispersionNode.disperseTwist )

	# inputTwist affects negativeTwist attribute.
	# inputTwist and jointNumber both affect twistDispersion attribute.
	TwistDispersionNode.attributeAffects ( TwistDispersionNode.inputTwist, TwistDispersionNode.negativeTwist )
	TwistDispersionNode.attributeAffects ( TwistDispersionNode.inputTwist, TwistDispersionNode.disperseTwist )
	TwistDispersionNode.attributeAffects ( TwistDispersionNode.jointNumber, TwistDispersionNode.disperseTwist )


def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Alexander Wagner", "1.0", "Any")
	try:
		mplugin.registerNode(
							 kAddUtilNodeTypeName,
							 kAddUtilNodeId,
							 nodeCreator,
							 nodeInitializer,
							 OpenMayaMPx.MPxNode.kDependNode,
							 kAddUtilNodeClassify
							 )
	except:
		sys.stderr.write( "Failed to register node: %s" % kAddUtilNodeTypeName )
		raise


def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( kAddUtilNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % kAddUtilNodeTypeName )
		raise
