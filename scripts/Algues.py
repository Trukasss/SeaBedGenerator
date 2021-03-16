# -*- coding: utf-8 -*-
import maya.cmds as cmds
import math
import random
#cmds.file(f=True, new=True)

#Suppression de la scene
def clear():
	cmds.select( all=True )
	cmds.delete()

# -------------------- Definision fonction dessCourbe --------------------
#Parametres : 
# - formule = "cLog", "cSin", "cDrt"
# - puissance = int ou float, je recommande 1
# - pDepart = liste de 3 elements int [0, 0, 0]
# - taille = int, je recommande 40
# - getX = int x de la position qu'on veut recuperer sur la courbe
def dessCourbe (formule, puissance, pDepart, taille, epaisseur, getX): 
    
    pDepX = pDepart[0]
    pDepY = pDepart[1]
    pDepZ = pDepart[2]
    c = cmds.curve (point = [tuple(pDepart)] )
    
    if (formule == "cLog"):
        for x in range(1, taille+1):
            cmds.curve( c, a=True, p=[(pDepX + math.log(x, puissance * 1.3), pDepY + x, pDepZ)] )
        getPosDeb = (pDepX + math.log(getX, puissance * 1.3), pDepY + getX, pDepZ)
        getPosFin = (pDepX + math.log(taille, puissance * 1.3), pDepY + taille, pDepZ)
                    
    if (formule == "cSin"):
        for x in range(1, taille+1):
            cmds.curve( c, a=True, p=[( (pDepX + math.sin(x) / x * puissance * 10) + math.log(x, puissance * 1.3), pDepY + x, pDepZ)] )
        getPosDeb = ( (pDepX + math.sin(getX) / getX * puissance * 10) + math.log(getX, puissance * 1.3), pDepY + getX, pDepZ )
        getPosFin = ( (pDepX + math.sin(taille) / taille * puissance * 10) + math.log(taille, puissance * 1.3), pDepY + taille, pDepZ )
                   
    if (formule == "cDrt"):
        for x in range(1, taille+1):
            cmds.curve( c, a=True, p=[(pDepX, pDepY + x, pDepZ)] )
        getPosDeb = (pDepX, pDepY + getX, pDepZ)
        getPosFin = (pDepX, pDepY + taille, pDepZ)
    
        
    cercle = cmds.circle( nr=(0, 1, 0), r=epaisseur )
    #cercle = cmds.polyPlane( w=0.1, h=0.1, sx=1, sy=1 )
    cmds.move(pDepart[0], pDepart[1], pDepart[2])
    cmds.rename("yo" + str(x))
    cmds.extrude( "yo" + str(x), c, et=2 )
    cmds.delete("yo" + str(x))
    
    cmds.delete(c)
    return getPosDeb, getPosFin


# -------------------- Definision fonction dessBranche --------------------
#Parametres : 
# - formule = "cLog", "cSin", "cDrt"
# - puissance = int ou float, je recommande 1
# - getPosDeb = liste de 3 elements int [0, 0, 0]
# - taille = int, je recommande 40
# - nbSousBranches = int
# - proportion = float (entre 0 et 1)
# - rotationBranche = int, degres
def dessBranche(formule, puissance, getPosDeb, taille, epaisseur, embout, nbSousBranches, proportion, rotationBranche):
    
    g_branche = cmds.group(empty = True, name = "branche")
    pIniRotate = tuple(getPosDeb)
   
    for i in range (1, nbSousBranches + 1):
        getX = int(taille * proportion)
        getPosDeb, getPosFin = dessCourbe( formule, puissance, getPosDeb, taille, epaisseur, getX)
        taille -= getX
        c = cmds.rename("branche_" + formule + "_" +  str(i))
        cmds.parent(c, g_branche)
        
        if (embout == 1):
            s = cmds.polySphere(sx=6, sy=6, radius = 2, n = "embout")
            cmds.polySoftEdge(a=180)
        elif (embout == 2):            
            s = cmds.polyCube(w=2, h=2, d=2, n = "embout")
            cmds.rotate(45, 0, 45)
        else :
            s = cmds.polyCone(ax=[0, -1, 0], r=2, sa=12, n = "embout")            
            cmds.polySoftEdge(a=60)
        
        cmds.move(getPosFin[0], getPosFin[1], getPosFin[2], s)
        cmds.parent(s, g_branche)
    
    cmds.rotate(0, rotationBranche, 0, g_branche , pivot = pIniRotate)
    return g_branche
    
# -------------------- Definision fonction colorierAlgue --------------------
def colorierAlgue(g_main, colo):
	#def shaders
	sh_tige = cmds.shadingNode("aiStandardSurface", name="mat_tige", asShader=True)
	cmds.setAttr(sh_tige+".baseColor",  0.87059,0.79216,0.63922)
	cmds.setAttr(sh_tige+".emissionColor",  0.87059,0.79216,0.63922)
	sh_embout = cmds.shadingNode('aiStandardSurface', name="mat_embout", asShader=True)
	cmds.setAttr(sh_embout+".baseColor", colo[0],  colo[1],  colo[2])
	cmds.setAttr(sh_embout+".emissionColor", colo[0],  colo[1],  colo[2])
	cmds.setAttr (sh_embout+".emission", 0.7)
	
	#attribution shader
	cmds.select(g_main)
	cmds.hyperShade(assign=sh_tige)
	
	#selection embout
	cmds.select(clear=True)
	for e in g_main:
		cmds.select("embout*", hi=True, add=True)
	cmds.hyperShade(assign=sh_embout)


# -------------------- Definision fonction dessAlgue --------------------
#Parametres : 

def dessAlgue(embout, puissance, tailleMin, tailleMax, epaisseur, nbBranchesMin, nbBranchesMax, nbSousBranchesMin, nbSousBranchesMax, proportionMin, proportionMax):
	#conversion de certaines valeurs	
	taille = random.uniform(tailleMin, tailleMax)
	taille /= 10
	nbBranches = random.randint(nbBranchesMin, nbBranchesMax)
	nbSousBranches = random.randint(nbSousBranchesMin, nbSousBranchesMax)
	proportion = random.uniform(proportionMin, proportionMax)
	
	#lancement de la construction de l'algue
	g_main = cmds.group(name="Algue", em=True)	    
	getPosDeb, getPosFin = dessCourbe ("cDrt", 1, [0,0,0], 10, epaisseur, 10)
	base = cmds.rename("base")
	cmds.parent(base, g_main)
	for i in range (0, nbBranches):
		rotDeg = 360/nbBranches
		g_branche = dessBranche ("cLog", puissance, getPosDeb, 35, epaisseur,embout, nbSousBranches, proportion, i*rotDeg)
		cmds.parent(g_branche, g_main)
	cmds.scale(taille, taille, taille, g_main, a=False)
	
	return g_main



#dessAlgue(1, 1, 1, 1, 5, 2, .5)

# -------------------- Interface --------------------
#cmds.window(title = "Generateur d'algues")
#cmds.columnLayout()

#UIembout = cmds.radioButtonGrp( label="Type d'embout", labelArray3=['Sphere', 'Cube', 'Cone'], numberOfRadioButtons=3, select=1 )
#UIpuissance = cmds.floatSliderGrp(field=True, label='puissance', minValue=0.2, maxValue=1, value=1, step=.1)
#UItailleMin = cmds.floatSliderGrp(field=True, label='tailleMin', minValue=0.1, maxValue=5, value=1.0)
#UItailleMax = cmds.floatSliderGrp(field=True, label='tailleMax', minValue=0.1, maxValue=5, value=1.0)
#UIepaisseur = cmds.floatSliderGrp(field=True, label='epaisseur', minValue=0.5, maxValue=2, value=1.0)
#UInbBranchesMin = cmds.intSliderGrp(field=True, label='nbBranchesMin', minValue=1, maxValue=10, value=2)
#UInbBranchesMax = cmds.intSliderGrp(field=True, label='nbBranchesMax', minValue=1, maxValue=10, value=2)
#UInbSousBranchesMin = cmds.intSliderGrp(field=True, label='nbSousBranchesMin', minValue=1, maxValue=5, value=2)
#UInbSousBranchesMax = cmds.intSliderGrp(field=True, label='nbSousBranchesMax', minValue=1, maxValue=5, value=2)
#UIproportionMin = cmds.floatSliderGrp(field=True, label='proportionMin', minValue=0.2, maxValue=.6, value=.5, step=0.1)
#UIproportionMax = cmds.floatSliderGrp(field=True, label='proportionMax', minValue=0.2, maxValue=.6, value=.5, step=0.1)

#cmds.button (label = "Grow!", c = "g_main = dessAlgue()")
#cmds.button (label = "select embouts!", c = "colorierAlgue(g_main)")
#cmds.button (label = "clear", c="clear()")
#cmds.showWindow()