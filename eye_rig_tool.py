import maya.cmds as mc


def eye_rig_tool(m_sel =mc.ls(sl=True)):
    """Select eyelid joints first then select vector up locator last."""
    jntPos_list = []
    
    for jnt in range(len(m_sel)-1):
    
        jnt_pos = mc.xform(m_sel[jnt], q=True, ws=True, t=True)
        jntPos_list.append(jnt_pos)
    
        
        
    for idx in range(len(jntPos_list)):
        jnt_name = mc.joint(m_sel[idx], q=True, name= True)
        new_loc_name = jnt_name.replace('_jnt_','_loc_')
        jntAim_loc = mc.spaceLocator(n=new_loc_name,p=jntPos_list[idx])
        mc.CenterPivot(jntAim_loc)   
        jnt_parent = mc.listRelatives(m_sel[idx], p=True)[0]
        mc.aimConstraint(
        jntAim_loc, 
        jnt_parent, 
        mo=True, 
        w=True, 
        aim=(1,0,0),
        u=(0,1,0),
        wut='object',
        wuo=m_sel[-1]
        )
    