import maya.cmds as mc

m_sel = mc.ls(sl=True)
eyelid_jnt_list = []
center_loc_pos = mc.xform(m_sel[-1], q=True,t=True, ws=True, a=True)

mc.select(cl=True)
print (m_sel[-1])
print(center_loc_pos)

for jnt in range(len(m_sel)-1):
    eyelid_jnt = m_sel[jnt]
    eyelid_jnt_list.append(eyelid_jnt)

print(eyelid_jnt_list)
    
for idx in range(len(eyelid_jnt_list)):
    jnt_name = mc.joint(eyelid_jnt_list[idx], q=True, name=True)
    print(jnt_name)
    new_jnt_name = jnt_name.replace('_jnt_','_offsetJnt_')
    print(new_jnt_name) 
    offset_jnt = mc.joint(n=new_jnt_name, p=center_loc_pos)
    mc.parent(eyelid_jnt_list[idx], offset_jnt)
    mc.joint(offset_jnt, e=True, rad = 0.25, oj='xyz', sao='yup', ch=1, zso=True)
    mc.joint(eyelid_jnt_list[idx], e=True, rad=0.25)
    mc.select(cl=True)