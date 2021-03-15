import maya.cmds as cmds
import maya.internal.common.cmd.base

nDeform = "waveDeform"

def deformation(amplitude=0.05, maxRadius=1.5):
    global nDeform
    if (not cmds.objExists(nDeform)):
        maya.internal.common.cmd.base.executeCommand('wave.cmd_create')
        cmds.deformer("wave1", e=True, n=nDeform)
    cmds.setAttr(nDeform+".amplitude", amplitude)
    cmds.setAttr(nDeform+".maxRadius", maxRadius)

def animerDeformation(vitesse=100):
    global nDeform
    nom = "waveDeformExpression"
    if(not cmds.objExists(nom)):
        cmds.expression(n = nom, s= nDeform+".offset = time1.outTime/"+str(vitesse))
    else:
        cmds.expression(nom, e=True, s= nDeform+".offset = time1.outTime/"+str(vitesse))

deformation(0.01)
animerDeformation()