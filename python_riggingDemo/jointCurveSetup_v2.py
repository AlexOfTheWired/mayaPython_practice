import maya.cmds as mc

def jointCurveSetup( prefix, jnt_num):

    m_sel = mc.ls(sl=True)

    loc_list = []
    jnt_list = []
    uNum = 1.0/(jnt_num-1)
    u_value_pos = 0.0

    mc.select(cl=True)

    # Create Locators
    print ('Creating locators...')
    for i in range(jnt_num):
        lIdx = '%s' %(i+1)
        loc_name = mc.spaceLocator(n='%s''%s''%s' %(prefix, "_loc_", lIdx))
        loc_list.append(loc_name)
        
    # Attaches Loctators to selected curve.
    print('Attaching locators to curve')
    for i in range(jnt_num):
        print (loc_list[i])
        mo_path = mc.pathAnimation(loc_list[i],m_sel, fractionMode=True, follow=True, bank=False)
        animCurvTL = mc.listConnections('%s''%s' %(mo_path,'.uValue'))[0]
        mc.delete(animCurvTL)
        mc.setAttr('%s''%s' %(mo_path,'.uValue'), u_value_pos)
        mc.cycleCheck(e=False)
        u_value_pos += uNum
        
    # Creates offset and control joints.
    print('Creating offset and control joints...')
    for i in range(jnt_num):
        jIdx = '%s' %(i+1)
        mc.select(loc_list[i])
        offest_jnt = mc.joint(n=('%s''%s''%s' %(prefix, '_offset_jnt_', jIdx)), r=0.25)
        control_jnt = mc.joint(n=('%s''%s''%s' %(prefix, '_control_jnt_', jIdx)), r=0.25)
        jnt_list.append(control_jnt)
        print (jnt_list)
    

        
