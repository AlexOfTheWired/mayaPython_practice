import maya.cmds as cmds


def rig_a_leg(lJoints=list()):

    y = 20.0
    for jnt in lJoints:
        cmds.joint(n=jnt, p=(5.0, y, 0.0))
        y -= 10.0

        # orient the Leg joints
    for jnt in lJoints:
        cmds.joint(jnt, e=True, oj='xyz', sao='yup', ch=True, zso=True)


def rig_a_spine(sJoints=list()):

    y = 20.0
    for jnt in sJoints:
        cmds.joint(n=jnt, p=(0.0, y, 0.0))
        y += 5.0

        # orient the Spine joints
    for jnt in sJoints:
        cmds.joint(jnt, e=True, oj='xyz', sao='yup', ch=True, zso=True)

def rig_an_arm(aJoints=list()):

    x=8.5
    for jnt in aJoints:
        cmds.joint(n=jnt, p=(x, 45.0, 0.0))
        x += 10.0

	    # orient the Arm joints
    for jnt in aJoints:
        cmds.joint(jnt, e=True, oj='xyz', sao='yup', ch=True, zso=True)



    # create ik handles
def leg_ik_maker():

    cmds.ikHandle(n='lf_leg_ik', sj='lf_hip_jnt', ee='lf_ankle_jnt', sol='ikRPsolver')
    cmds.setAttr('%s.preferredAngleZ' % 'lf_knee_jnt', -20.0)
    cmds.ikHandle(n='lf_ball_ik', sj='lf_ankle_jnt', ee='lf_ball_jnt', sol='ikSCsolver')
    cmds.setAttr('%s.preferredAngleZ' % 'lf_knee_jnt', -20.0)
    cmds.ikHandle(n='lf_toe_ik', sj='lf_ball_jnt', ee='lf_toe_jnt', sol='ikSCsolver')
    cmds.setAttr('%s.preferredAngleZ' % 'lf_toe_jnt', -20.0)


rig_a_leg(['lf_hip_jnt','lf_knee_jnt', 'lf_ankle_jnt', 'lf_ball_jnt', 'lf_toe_jnt'])
rig_a_spine(['spineA_jnt', 'spineB_jnt', 'spineC_jnt', 'spineD_jnt', 'spineE_jnt', 'spineF_end'])
rig_an_arm(['lf_shoulder_jnt', 'lf_elbow_jnt', 'lf_wrist_jnt', 'lf_wrist_end'])

cmds.mirrorJoint('lf_hip_jnt', mirrorYZ=True, mirrorBehavior=True, searchReplace=('lf_', 'rt_'))

def knee_controller():
    cmds.spaceLocator(n='lf_knee_ctrl', p=( 5.0, 10.0, 8.0))
    cmds.poleVectorConstraint('lf_knee_ctrl', 'lf_leg_ik')

knee_controller()

cmds.ikHandle(n='spine_ik', sj='spineA_jnt',ee='spineF_end', ccv=True, sol='ikSplineSolver')
cmds.setAttr('%s.preferredAngleZ' % 'spineC_jnt', -20.0)

cmds.parent('lf_hip_jnt', 'spineA_jnt')
cmds.parent('rt_hip_jnt', 'spineA_jnt')
