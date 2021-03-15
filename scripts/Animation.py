import maya.cmds as cmds
import maya.internal.common.cmd.base

#--------------------- ANIMATION DEFORMEUR ---------------------

#Variable globale avec le nom du deformeur
nDeform = "waveDeform"

#Fonction qui permet de créer un le deformeur wave avec deux parametres facultatifs ou de changer ces deux parametres si le deformeur existe deja.
def deformation(amplitude, maxRadius):
    global nDeform
    if (not cmds.objExists(nDeform)):
        maya.internal.common.cmd.base.executeCommand('wave.cmd_create')
        cmds.deformer("wave1", e=True, n=nDeform)
    cmds.setAttr(nDeform+".amplitude", amplitude)
    cmds.setAttr(nDeform+".maxRadius", maxRadius)

#Fonction qui permet d'animer l'offset du deformeur du meme nom, en le liant via une expression au temps.
#Le rapport est divise par un parametre (par default 100) lenteur qui divise le temps par la valeur indiquee.
def animerDeformation(lenteur):
    global nDeform
    nom = "waveDeformExpression"
    if(not cmds.objExists(nom)):
        cmds.expression(n = nom, s= nDeform+".offset = time1.outTime/"+str(lenteur))
    else:
        cmds.expression(nom, e=True, s= nDeform+".offset = time1.outTime/"+str(lenteur))

def selObjVagues():
    pass

def boutonAnimerVagues(amplitude=0.05, maxRadius=1.5, lenteur=100):
    selObjVagues()
    deformation(amplitude, maxRadius)
    animerDeformation(lenteur)

#--------------------- ANIMATION BOIDS ---------------------