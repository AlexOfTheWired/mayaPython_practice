
def locator_placement_tool(m_sel=mc.ls(sl=True),prefix = 'Test'):
    
    jnt_pos_list = []
    loc_grp = mc.createNode('transform', name = '%s_faceLocator_grp' % (prefix))
    
    for jnt in range(len(m_sel)):
        jnt_pos = mc.xform(m_sel[jnt], q=True, t=True, ws=True, a=True)
        jnt_pos_list.append(jnt_pos)
        
    for idx in range(len(jnt_pos_list)):
        x_pos = jnt_pos_list[idx][0]
        y_pos = jnt_pos_list[idx][1]
        z_pos = jnt_pos_list[idx][2]

        
        face_loc = mc.spaceLocator(p = (x_pos, y_pos, z_pos))
        mc.CenterPivot(face_loc)
        mc.makeIdentity(face_loc)
        mc.parent(m_sel[idx], face_loc)
        mc.parent(face_loc, loc_grp)