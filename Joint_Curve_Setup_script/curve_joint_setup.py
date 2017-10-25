import maya.cmds as mc


def attach_loc_to_curve(prefix, loc_num):
    """This function creates Locators and attaches 
    them to a curve with a uniform distance between each Locator"""

    sel = mc.ls(sl=True)
    
    curve_selection = []        
    uNum = 1.0/(loc_num-1)
    u_value_pos = 0.0
    
    for loc in range(loc_num):
        print(u_value_pos)
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
        mc.setAttr(mo_path + '.uValue', u_value_pos)
        u_value_pos += uNum
        mc.cycleCheck(e=False)
        offset_jnt = mc.joint(n=(prefix + '_offsetJnt_' + lIdx), r=0.25)
        control_jnt = mc.joint(n=(prefix + '_controlJnt_' + lIdx), r=0.25)
        control_obj = mc.sphere(n=(prefix + '_control_' + lIdx), r=0.25)
        mc.parent(control_obj, loc_name, s=True, r=True)
        mc.parentConstraint(control_obj, control_jnt,  weight=1)
        
        
attach_loc_to_curve('l_brow_curve', 3)
