import maya.cmds as mc
import maya.OpenMaya as om

help(maya.OpenMaya.MObject)

def preSetup():
    selectionList = om.MSelectionList()
    dagPath = om.MDagPath()
    fnTransform = om.MFnTransform()
    
    om.MGlobal.getActiveSelectionList(selectionList)
    if selectionList.length() >= 1:
        try:
            selectionList.getDagPath(0,dagPath)
            fnTransform.setObject(dagPath)
            listLength = selectionList.length()
            print(listLength)
        except:
            print('Select A Transform Node.')
            return
    else:
        print('Select A TransformNode.')
        return
        
    transformMatrix = fnTransform.transformation()
    
    print(transformMatrix)

preSetup()

###############################################################
## Maya Python API 2.0
###############################################################

import maya.api.OpenMaya as om2

def preSetup2():
    #selectionList = om2.MSelectionList()
    dagPath = om2.MDagPath()
    fnTransform = om2.MFnTransform()
    
    activeList = om2.MGlobal.getActiveSelectionList()
    aListLength = activeList.length()
    print(aListLength)


    
    if activeList.length() >= 1:
        try:
            for idx in xrange(aListLength):
                DagPath = activeList.getDagPath(idx)
                fnTransform.setObject(DagPath)
                print(DagPath)

            print("NOICE!!!")
        except:
            print('Select A Transform Node.')
            return
    else:
        print('Select A TransformNode.')
        return
        
    transformMatrix = fnTransform.transformation()
    print(transformMatrix)

preSetup2()
