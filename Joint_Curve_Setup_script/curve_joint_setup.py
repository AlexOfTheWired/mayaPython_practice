import maya.cmds as mc

def attach_loc_to_curve(prefix, loc_num):
    """This function creates Locators and attaches 
    them to a curve with a uniform distance between each Locator"""

    sel = mc.ls(sl=True)
    
    curve_selection = []        
    uNum = 1.0/(loc_num-1)
    uMin = 0.0
    for loc in range(loc_num):
        uMin += uNum
        print(uMin)
        lIdx = '%s' % (loc+1) 
        loc_name = mc.spaceLocator(n=(prefix + "_loc_" + lIdx))
        curve_selection.append(loc_name)
        print(curve_selection)
        mo_path = mc.pathAnimation(
                                    loc_name[0],sel, 
                                    fractionMode=True, 
                                    follow=True, 
                                    followAxis='x', 
                                    upAxis='y', 
                                    worldUpType='vector', 
                                    worldUpVector=(0, 1, 0), 
                                    inverseUp=False, 
                                    bank=False
                                    )
        animCurvTL = mc.listConnections(mo_path + '.uValue')[0]
        mc.delete(animCurvTL)
        mc.setAttr(mo_path + '.uValue', uMin)
        


# Create a control group for every locator ===> mc.createNode()

# For every control group create a main joint and an offset joint ====> mc.joint()

# for every offset Joint create a Control Object ===> (NURBS Circle, Nurbs Sphere, etc...)


        
#animCurvTL = mc.listConnections(MoPath + '.uValue')[0]
#mc.disconnectAttr(animCurvTL + '.output', theMoPath + '.uValue')
#mc.delete(animCurvTL)
    
    
attach_loc_to_curve('test', 5)

mc.pathAnimation()