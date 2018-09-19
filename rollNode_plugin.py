import sys
import math
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kAddUtilNodeTypeName = "Rolling"
kAddUtilNodeClassify = "utility/general"
kAddUtilNodeId = OpenMaya.MTypeId(0x87327)

class rtAddUtilNode(OpenMayaMPx.MPxNode):
	
	
	
	input  = OpenMaya.MObject()
	translate1 = OpenMaya.MObject()
	radius = OpenMaya.MObject()
	output = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def compute(self, plug, dataBlock ):
		if plug == rtAddUtilNode.output:

			try:
				input_dataHandle1 = dataBlock.inputValue( rtAddUtilNode.translate1 )
			except:
				sys.stderr.write( "Failed to get MDataHandle inputValue translate1" )
				raise
			try:
				input_dataHandle2 = dataBlock.inputValue( rtAddUtilNode.radius )
			except:
				sys.stderr.write( "Failed to get MDataHandle inputValue radius" )
				raise
			try:
				output_dataHandle = dataBlock.outputValue( rtAddUtilNode.output )
			except:
				sys.stderr.write( "Failed to get MDataHandle outputValue output" )
				raise

			pi = math.pi
			translate_value1 = input_dataHandle1.asFloat()
			radius_value = input_dataHandle2.asFloat()

			result = (translate_value1 / (-radius_value)) * (180 / pi)
			output_dataHandle.setFloat(result)
			dataBlock.setClean(plug)

		else:
			return OpenMaya.MStatus.kSuccess


def nodeCreator():
	return OpenMayaMPx.asMPxPtr( rtAddUtilNode() )

def nodeInitializer():
	nAttr = OpenMaya.MFnNumericAttribute()

	rtAddUtilNode.translate1 = nAttr.create("translate1", "t", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)

	rtAddUtilNode.radius = nAttr.create("radius", "ra", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)

	rtAddUtilNode.output = nAttr.create("output", "o", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)

	rtAddUtilNode.addAttribute( rtAddUtilNode.translate1)
	rtAddUtilNode.addAttribute( rtAddUtilNode.radius)
	rtAddUtilNode.addAttribute( rtAddUtilNode.output)

	rtAddUtilNode.attributeAffects ( rtAddUtilNode.translate1, rtAddUtilNode.output )
	rtAddUtilNode.attributeAffects ( rtAddUtilNode.radius, rtAddUtilNode.output )


def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Alex Wagner", "1.0", "Any")
	try:
		mplugin.registerNode(
							 kAddUtilNodeTypeName,
							 kAddUtilNodeId,
							 nodeCreator,
							 nodeInitializer,
							 OpenMayaMPx.MPxNode.kDependNode,
							 kAddUtilNodeClassify)
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
