
import maya.cmds as mc

def createStretchyIkSpine(s_curve=mc.ls(sl=True), jnt_num=3):
    """
    Creates a stretchy Ik Spine from a selected or specified curve.
    """    
    if not s_curve:
        mc.error('No curve specified or selected')
    else:
        s_curve = s_curve[0]
    if jnt_num < 2:
        mc.error('Must have at least two joints')
    
    jnt_list = []
    
    mc.select(cl=True)
    
    for i in range(jnt_num):
        s_idx  = '%s' % (i+1)
        strJnt = mc.joint(n='%s_jnt_%s'%(s_curve,s_idx))
        jnt_list.append(strJnt)
    
        
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
    s_curve_node = mc.createNode('curveInfo', n='%s_curveInfo' % (s_curve))
    s_multi_node = mc.createNode('multiplyDivide', n='%s_divide' % (s_curve))

    mc.setAttr( '%s.operation'%(s_multi_node), 2)
    mc.setAttr( '%s.input2X'%(s_multi_node), g_arclen)
    
    mc.connectAttr( '%s.arcLength'%(s_curve_node), '%s.input1X'%(s_multi_node))
    
    mc.connectAttr('%sShape.worldSpace'%(s_curve), '%s.inputCurve'%(s_curve_node))
    
    for i in range(jnt_num):
        if i > 0:
            mc.setAttr('%s.tx'%(jnt_list[i]), g_average)
            
    for jnt in jnt_list:
        mc.connectAttr('%s.outputX'%(s_multi_node), '%s.scaleX'%(jnt))