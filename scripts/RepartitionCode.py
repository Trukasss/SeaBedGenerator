# -*- coding: utf-8 -*-
import maya.cmds as cmds
import math
import random

cmds.file(f=True,new=True)

# ------------------ REPARTITION AU SOL ------------------
#param: nom de l'objet a instancier (type = chaine de caractere)
#       sur quel support? (type = chaine de caractere)
#       nb d'instance 
#       la rotation 

# ------- Repartition -------
def Repartition(obj,target,quantity,rotation,scale_min, scale_max):
    # ------- Groupes
    g=cmds.group(em=True, n="gr_"+obj)
    gL=cmds.group(em=True, n="grLocators")
    
    #recuperation valeur des sliders
   
    for i in range(1,quantity + 1):

        if(target == "fond"):
            r= random.randrange(1,4000)
        else :
            r= random.randrange(1,cmds.polyEvaluate(target, v= True))
        # ------- Recuperation du nombre de vertex du Sol
        rT = cmds.polyEvaluate(v=True)
        p1=cmds.xform(target+".vtx["+str(r)+"]", q=True, translation=True, worldSpace=True)
        
        # ------- instance des objets
        obji=cmds.duplicate(obj, n=obj+str(i))
        print(obji)
        cmds.move(p1[0],p1[1],p1[2], obj+str(i), r=True)
        scaleI= random.uniform(scale_min,scale_max)
        cmds.scale(scaleI,scaleI,scaleI,obj+str(i))
        
        # ------- coordonnees de la normal du vertex
        cmds.select(target+".vtx["+str(r)+"]")
        vn1 = cmds.polyNormalPerVertex(q=True, xyz=True)
        
        # ------- creation du locator
        l=cmds.spaceLocator(n="locator"+str(i))
        cmds.move(p1[0], p1[1], p1[2], r=True)
        cmds.xform(rp=(vn1[0],vn1[1],vn1[2]))
        
        # ------- aim constraint
        cmds.select("locator"+str(i),r=True)
        cmds.select(obj+str(i), tgl=True)
        cmds.aimConstraint(offset=(0,0,0), weight=1, aimVector=(0,1,0), worldUpType="vector", worldUpVector=(0,1,0))
        
        
        cmds.parent(obji[0],g)
        cmds.parent(l,gL)
        cmds.select("grLocators")
        #cmds.hide()
        
        
    
        cmds.rotate(0,rotation ,0, obj+str(i))
    
    cmds.delete("grLocators") #*|*"
    cmds.delete(obj)

# ------------------ INTERFACE ------------------

#cmds.window("Generateur de fond marin")
#cmds.columnLayout()


# ------- Repartition
#sliderNbAlgue = cmds.intSliderGrp( field=True, label="Nombre d'algues", minValue=5, maxValue=200, value=5)
#sliderRotAlgue = cmds.intSliderGrp( field=True, label="Rotation des algues", minValue=1, maxValue=15, value=1)
#slider6 = cmds.intSliderGrp( field=True, label="Rotation des rochers", minValue=0, maxValue=100, value=0)

#cmds.button(label="Generer",c="Repartition('Algue','fond',sliderNbAlgue,sliderRotAlgue)")



    
