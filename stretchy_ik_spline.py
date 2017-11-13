import maya.cmds as mc

def createStretchyIkSpine(s_curve, jnt_num):
    """
    Creates a stretchy Ik Spine from a selected or specified curve.
    """    
    
    if s_curve =='':
        s_curve = mc.ls(sl=True)[0]
        
    jnt_list = []
    
    mc.select(cl=True)
    
    for i in range(jnt_num):
        s_idx  = '%s' % (i+1)
        strJnt = mc.joint(n=s_curve + '_jnt_' + s_idx)
        jnt_list.append(strJnt)
    
    # This probably isn't needed.    
    #for jnt in jnt_list:
    #    mc.setAttr('%s.preferredAngleZ' % (jnt), -20.0)
        
    s_curveIk = mc.ikHandle(
                            sj=jnt_list[0], 
                            ee=jnt_list[-1], 
                            c=s_curve, 
                            n=s_curve + '_ik', 
                            sol='ikSplineSolver', 
                            ccv=False, 
                            rootOnCurve=True, 
                            parentCurve=False
                           )[0]   
    
    g_arclen     = mc.arclen(s_curve)
    g_average    = g_arclen/(jnt_num-1) 
    s_curve_node = mc.createNode('curveInfo', n=s_curve + '_curveInfo')
    s_multi_node = mc.createNode('multiplyDivide', n=s_curve + '_divide')

    mc.setAttr(s_multi_node + '.operation', 2)
    mc.setAttr(s_multi_node + '.input2X', g_arclen)
    
    mc.connectAttr(s_curve_node + '.arcLength', s_multi_node + '.input1X')
    
    mc.connectAttr(s_curve + 'Shape.worldSpace', s_curve_node + '.inputCurve')
    
    for i in range(jnt_num):
        if i > 0:
            mc.setAttr(jnt_list[i] + '.tx', g_average)
            
    for jnt in jnt_list:
        mc.connectAttr(s_multi_node + '.outputX', jnt + '.scaleX')
        
    # Hello, Nick