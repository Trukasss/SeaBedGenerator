# -*- coding: utf-8 -*-
import maya.cmds as cmds
import math
import random

cmds.file(f = True, new = True)

# ------------------ REPARTITION AU SOL ------------------
#param: nom de l'objet à instancier (type = chaine de caractère)
#       sur quel support? (type = chaine de caractère)
#       nb d'instance 
#       la rotation 

# ------- Repartition -------
def Repartition(obj, target, quantity, rotation, scale_min, scale_max):
    
    # ------- Listes position
    already_seen = set() # liste des place déjà prises
    created = []
    
    # ------- Groupes
    g = cmds.group(em = True, n = "gr_" + obj)
    gL = cmds.group(em = True, n = "grLocators")
    
    
    #recuperation valeur des sliders
    for i in range(1, quantity + 1):
        if(target == "fond"):
            pos = random.randrange(1, 4000)
            
        else :
            pos = random.randrange(1, cmds.polyEvaluate(target, v = True))
            
        # ------- Récupération du nombre de vertex du Sol
        rT = cmds.polyEvaluate(v=True)
        p1 = cmds.xform(target + ".vtx[" + str(pos) + "]", q = True, translation = True, worldSpace = True)
        
        # ------- Instance des objets
        boundbox = cmds.exactWorldBoundingBox(obj)
        obji = cmds.instance(obj, n = obj + str(i))
        
        if (p1[0], p1[2], p1[2]) not in already_seen:
            already_seen.add((p1[0], p1[1], p1[2]))
            print(already_seen)
            
            cmds.move(p1[0], p1[1], p1[2], obj + str(i), r = True)
            
            created.append(already_seen)
            print(created)
            
        scaleI = random.uniform(scale_min, scale_max)
        cmds.scale(scaleI, scaleI, scaleI, obj + str(i))
        
        # ------- coordonnees de la normal du vertex
        cmds.select(target + ".vtx[" + str(pos) + "]")
        vn1 = cmds.polyNormalPerVertex(q = True, xyz = True)
        
        # ------- creation du locator
        l = cmds.spaceLocator(n = "locator" + str(i))
        cmds.move(p1[0], p1[1], p1[2], r = True)
        cmds.xform(rp = (vn1[0], vn1[1], vn1[2]))
        
        # ------- aim constraint
        cmds.select("locator" + str(i), r = True)
        cmds.select(obj + str(i), tgl = True)
        cmds.aimConstraint(offset = (0, 0, 0), weight = 1, aimVector = (0, 1, 0), worldUpType = "vector", worldUpVector = (0, 1, 0))
        
        
        cmds.parent(obji, g)
        cmds.parent(l, gL)
        cmds.select("grLocators")
        #cmds.hide()
        
        
    
        cmds.rotate(0, rotation, 0, obj + str(i))
    
    cmds.delete("grLocators") #*|*"
    cmds.delete(obj)
    
    
    # ------- Delete empty group ------- 
    transforms =  cmds.ls(type = "transform")
    deleteList = []
    
    for grp in transforms:
        if cmds.nodeType(grp) == "transform":
            children = cmds.listRelatives(grp, c = True)
            if children == None:
                print "%s, had no children and was deleted" %(grp)
                deleteList.append(grp)
     
    if len(deleteList) > 0:
       cmds.delete(deleteList)


# ------------------ CLEAN SCENE ------------------ 
 
def clean():
    cmds.file(f = True, new = True)
