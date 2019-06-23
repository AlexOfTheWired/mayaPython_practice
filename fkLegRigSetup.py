import maya.cmds as mc

leg_joint_list = mc.ls(sl=True)

fk_leg_joint_list = mc.duplicate(leg_joint_list,rc=True)
print(fk_leg_joint_list)

for idx in xrange(len(fk_leg_joint_list)):
    fk_node_name = fk_leg_joint_list[idx].replace('_jnt_02','_FK_jnt_01')
    mc.rename(fk_leg_joint_list[idx],fk_node_name)
    fk_leg_joint_list[idx] = fk_node_name