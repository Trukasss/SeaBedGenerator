# -*- coding: utf-8 -*-
import maya.cmds as cmds
import random as rand
#from SeaBedGenerator.scripts.main import setImport
# from SeaBedGenerator.scripts import RepartitionCode
# reload(RepartitionCode)

#variable globale
count = 0 #nombre de fois ou on clique sur "create shoal"


def shoal(n, colo, nbFish, espacementFish, scaleFish, nomType):
    lar = 14 #taille du terrain qui variera en fonction du terrain
    long = 14
    
    #groupe qui regroupe les poissons du bancs 
    grFish = cmds.group(em=True, n="grp_fishy"+str(n))
    
    #generation de plusieurs fish 
    for i in range(0,nbFish):
       r1 = rand.uniform(-espacementFish/2.0, espacementFish/2.0)
       r2 = rand.uniform(-espacementFish/2.0, espacementFish/2.0)
       r3 = rand.uniform(-espacementFish/2.0, espacementFish/2.0)
       cmds.move(r1,r2,r3, nomType)  
       cmds.rotate(rand.uniform(-20,20),rand.uniform(-20,20),0, nomType)
       cmds.scale(scaleFish,scaleFish,scaleFish,nomType) 
       f = cmds.instance(nomType, leaf=True)
       cmds.parent( f, grFish)
       
    #------------ REPARTITION ici -------------------
    randomY = rand.uniform(4,8) #?gerer la hauteur
    cmds.move(rand.uniform(-lar/2,lar/2),randomY,rand.uniform(-long/2,long/2), grFish) #repartition dans l'espace sur un plan
    cmds.rotate(rand.uniform(-15,15),rand.uniform(-180,180),0, grFish)
   
    
    cmds.select(nomType)
    cmds.delete(nomType)  
    
    applyColor(nomType, colo)

def applyMaterial(obj, r, g, b):
    if cmds.objExists(obj):
        shd = cmds.shadingNode('blinn', name=obj + "_lambert", asShader=True)
        shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
    #voila faut juste rajouter cette ligne
        cmds.setAttr("%s.color" %shd, r, g, b)
        cmds.sets(obj, e=True, forceElement=shdSG)

def applyMaterialv2(obj, r, g , b):
     #if cmds.objExists(obj):
    mat = cmds.shadingNode('aiStandardSurface', name="mat", asShader=True)
    cmds.setAttr(mat+".baseColor", r, g, b)
    cmds.setAttr(mat+".emissionColor", r, g ,b)
    cmds.select(obj)
    cmds.hyperShade(assign= mat)

def applyColor(nomType, colo):
    #--- definition du nom du type de poisson a instancier ---
    
    Nag = cmds.shadingNode('aiStandardSurface', name="na", asShader=True)
    cmds.setAttr(Nag+".baseColor", 0.87059,0.79216,0.63922)
    cmds.setAttr(Nag+".specularRoughness", 0.8)
    
    Body = cmds.shadingNode('aiStandardSurface', name="bo", asShader=True)
    cmds.setAttr(Body+".baseColor", colo[0], colo[1],colo[2])#colo[0], colo[1],colo[2]
    cmds.setAttr(Body+".specularRoughness", 0.8)
    cmds.setAttr(Body+".emission", 0.6)
    cmds.setAttr(Body+".emissionColor", colo[0], colo[1],colo[2])
    
    #attribution poissons
    cmds.select(nomType+"*|"+nomType+"_corps*",  hi=True, add=True)
    cmds.hyperShade(assign=Nag)
    #cmds.hyperShade(assign = )
    #applyMaterialv2(ok, rand.uniform(0,1), rand.uniform(0,1), rand.uniform(0,1))   
    #selection nageoires
    
    cmds.select(clear=True)
    cmds.select(nomType+"*|"+nomType+"_nageoires*",  hi=True, add=True) 
    cmds.hyperShade(assign=Body)
    #applyMaterialv2(nageoires, rand.uniform(0,1), rand.uniform(0,1), rand.uniform(0,1))
    
    
#INTERFACE
#cmds.window(title="Shoal Generator")
#cmds.columnLayout()
#SliderNbFish = cmds.intSliderGrp(field=True,label="Number of fish per shoal", maxValue=20, minValue =6 , value=10, step=1.0)
#SliderEspaceFish = cmds.floatSliderGrp(field=True,label="Space between fish", maxValue=6, minValue =3 , value=3.5, step=0.3)
#SliderNbShoal = cmds.intSliderGrp(field=True,label="Number of shoal", maxValue=10, minValue =1 , value=3, step=1.0)
#SliderScaleFishy = cmds.floatSliderGrp(field=True,label="Scale of Fish", maxValue=1, minValue =0.2 , value=0.5, step=0.1)
#typeFish = cmds.radioButtonGrp(numberOfRadioButtons=2, label='Type of fish', labelArray2=['Long One', 'Round One'] )




#cmds.button(label="Create Shoal", c="count = multiple(count)")
#cmds.button(label="ApplyColorToFish", c="applyColor()")
#cmds.button(label="Clean", c="clean()")
#cmds.showWindow()


