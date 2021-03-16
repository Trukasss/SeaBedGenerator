# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.internal.common.cmd.base

#_______________________ ANIMATION DEFORMEUR _______________________#

#Variable globale avec le nom du deformeur
nDeform = "waveDeform"

#Fonction qui permet de creer un le deformeur wave avec deux parametres facultatifs ou de changer ces deux parametres si le deformeur existe deja.
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

def boutonAnimerVagues(grpAnimVague, amplitude=0.05, maxRadius=1.5, lenteur=100):
    cmds.select(grpAnimVague)
    deformation(amplitude, maxRadius)
    animerDeformation(lenteur)

#_______________________ ANIMATION BOIDS _______________________#
cmds.file(new=True, f=True)
import math

#------scene init------#
def getPos(obj):
    return (cmds.xform(obj, q=True, t=True, ws=True))

def getDis(pA, pB):
    dis = math.sqrt( abs( pow((pB[0]-pA[0]), 2) + pow((pB[1]-pA[1]), 2) + pow((pB[2]-pA[2]), 2) ) )
    return dis

def getNormVec(pA, pB):
    vecX = abs(pA[0] - pB[0])
    vecY = abs(pA[1] - pB[1])
    vecZ = abs(pA[2] - pB[2])
    dis = getDis(pA, pB)
    vecX /= dis
    vecY /= dis
    vecZ /= dis
    return(vecX, vecY, vecZ, dis)

def boidSep(sujet, proche):
    pA = getPos(sujet)
    pB = getPos(proche)
    if(getDis(pA, pB) < disTol):
        dirAB = getNormVec(pA, pB)
        cmds.move(-dirAB[0]*vit/dirAB[3], -dirAB[1]*vit/dirAB[3], -dirAB[2]*vit/dirAB[3], sujet, r=True)
        print("dirAB = " +str(dirAB))
    else:
        print("trop loin")

def simulerBoids(sujet, proche, temps):
    temps = int(temps)
    for i in range(1, temps+1):
        cmds.currentTime(i)
        cmds.setKeyframe(sujet, at=["tx", "ty", "tz"], t=i)

        boidSep(sujet, proche)

#------scene init------#
vit = 0.5
disTol = 20
rSph = cmds.polySphere()
cmds.move(0, 0, 1, rSph, a=True)
rCub = cmds.polyCube()
cmds.move(3, 0, 4, rCub, a=True)

# print("Distance = " +str(getDis(getPos(rSph), getPos(rCub))))
# print(getNormVec(getPos(rSph), getPos(rCub)))

simulerBoids(rSph, rCub, 10)



