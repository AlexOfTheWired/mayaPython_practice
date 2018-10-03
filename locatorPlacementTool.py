import maya.cmds as mc

def face_loc_placer(m_sel = mc.ls(sl=True)):    
    """This function takes positions of target joints and creates locator 
    on top of them, and parents the joint to the locators and them to a group.
    """
    
    jnt_pos_list = []
    loc_grp = mc.createNode( 'transform', name='Bruce_loc_grp')
    
    for idx in range(len(m_sel)):
        # get eash joint pos 
        jnt_pos = mc.xform(m_sel[idx],q=True, t=True, ws=True, a=True )
        # assign pos to list
        jnt_pos_list.append(jnt_pos)
    
    for idx in range(len(jnt_pos_list)):
        # assign joint name to a variable
        jnt_name = mc.joint(m_sel[idx],q=True, name=True)
        #assign new locator name to variable
        loc_name = jnt_name.replace('_jnt_','_loc_')
        # assign x position value to variable
        x_pos = jnt_pos_list[idx][0]
        # assign y position value to variable
        y_pos = jnt_pos_list[idx][1]
        # assign z position value to variable
        z_pos = jnt_pos_list[idx][2]
        
        face_loc = mc.spaceLocator(n=loc_name, p=(x_pos,y_pos,z_pos))
        mc.CenterPivot(face_loc)
        mc.parent( m_sel[idx], face_loc)
        mc.parent(face_loc, loc_grp)


