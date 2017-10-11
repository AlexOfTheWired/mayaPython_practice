import maya.cmds as mc

def joint_curve_setup(num, prefix):
    if num == 1:
        fullName = mc.rename("curve1", (prefix + "_curve"))
        mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        mc.DeleteHistory()
        mc.CenterPivot()
        mc.select(cl=True)
        mc.spaceLocator(p=(0, 0, 0))
        locName = mc.rename("locator1" + "_loc_01")
        mc.select(fullName, tgl=True)
        mc.pathAnimation(
                        fm=True,
                        f=True,
                        fa="x",
                        ua="y",
                        wut="vector",
                        wu=(0, 1, 0))
