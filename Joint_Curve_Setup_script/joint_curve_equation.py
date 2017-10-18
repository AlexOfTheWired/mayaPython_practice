import maya.cmds as mc

def iterative_number_addition(iNum):
  
    uMin = 0.0
    
    uNum = 1.0/iNum
  
    for i in range(iNum):
        if uMin < 1:
            uMin += uNum
            print uMin
  
    print (uNum)
  

iterative_number_addition(3)


