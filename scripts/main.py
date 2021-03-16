# -*- coding: utf-8 -*-
import maya.cmds as cmds
import random
import math
import mtoa.utils as mutils
import mtoa.core as core


#__________________ nos codes __________________
from SeaBedGenerator.scripts import imports
reload(imports)
from SeaBedGenerator.scripts.Sol import Fond
from SeaBedGenerator.scripts.fish import shoal
from SeaBedGenerator.scripts.Algues import dessAlgue, colorierAlgue
from SeaBedGenerator.scripts.RepartitionCode import Repartition
from SeaBedGenerator.scripts import Animation
reload(Animation)


cmds.file(f=True, new=True)

# __________________ definition de variables globales _______________________
count = 0 #nombre de fois qu'on clique sur "create shoal"

#J'ai rentre le chemin d'acces dans une variable string. Maintenant il suffit de changer l'endroit qu'une seule fois.
pathVignettes = cmds.internalVar(usd=True)+"SeaBedGenerator/Vignettes/"
pathImport= cmds.internalVar(usd=True)+"SeaBedGenerator/Models/"
grpAnimVague = []

#__________imports_________
#param = le nom du FBX
def setImport(nomAsset):
    setImportPath = pathImport + nomAsset
    cmds.file(setImportPath, i=True, mergeNamespacesOnClash=True, namespace=':')
# __________________________ FONCTION pour le choix des Coraux __________________________________
def choixCoraux():
    #________definir les type de coraux_________
    if (cmds.radioButtonGrp(typeCoraux, q=True, select=True) == 1):
        setImport("CorailCone_complexe.fbx")
        setImport("CorailCone_double.fbx")
        setImport("CorailCone_triple.fbx")
        setImport("CorailCone_double.fbx")
    if (cmds.radioButtonGrp(typeCoraux, q=True, select=True) == 2):
        setImport("CorailPhone_seul.fbx")
        setImport("CorailPhone_triple.fbx")


# __________________________ FONCTIONS pour importer �l�ments + appeler la r�partition des �l�ments __________________________________
def repartirRochers(nb, rotation, scale_min, scale_max, colo):
    if cmds.objExists("Rocher*"):
        cmds.delete("Rocher*")
    #-----import des rochers
    setImport('Rocher_enorme.fbx')
    setImport('Rocher_gros.fbx')
    setImport('Rocher_moyen.fbx')
    setImport('Rocher_petit.fbx')

    #-----g�rer le nb d'instance par type de rochers TROUVER UN ALGO POUR LA REPARTITION
    #if (nb%2 == 0): #pair
    #    nbP = nb / 4
    #    nbM = nb / 4
    #    nbG = nb / 4
    #    nbE = nb / 4
    #else:
    #    nbP = ((nb-1) / 4) +1
    #    nbM = (nb-1) / 4
    #    nbG = (nb-1) / 4
    #   nbE = (nb-1) / 4
    nbP = nb / 2
    nbM = nb / 2
    nbG = 2
    nbE = 1

    #----- appel de la fonction de r�partition
    Repartition('Rocher_enorme','fond',nbE, rotation, scale_min, scale_max)
    Repartition('Rocher_gros','fond',nbG, rotation, scale_min, scale_max)
    Repartition('Rocher_moyen','fond',nbM, rotation, scale_min, scale_max)
    Repartition('Rocher_petit','fond',nbP, rotation, scale_min, scale_max)

    cmds.select("Rocher*")
    listeRock= cmds.ls(sl=True, fl=True)
    cmds.polyUnite(listeRock, n="Rochers")

    #_______ application couleurs ________#

    ApplyColor("Rocher", colo, 0)


def repartirCoquillages(nb, rotation, scale_min, scale_max, colo):
    if cmds.objExists("Coquillage*"):
        cmds.delete("Coquillage*")

    #-----import du mesh coquillage
    setImport('Coquillage.fbx')

    #----- appel de la fonction de r�partition
    Repartition('Coquillage','fond', nb, rotation, scale_min, scale_max)

    #_______ application couleurs ________#
    ApplyColor("Coquillage", colo, 0)

def repartirOursins(nb, rotation,scale_min,scale_max, colo):
    if cmds.objExists("Oursin*"):
        cmds.delete("Oursin*")
        #cmds.delete("grOursin*")
    #-----import du mesh oursins
    setImport('Oursin.fbx')


    #----- appel de la fonction de r�partition
    Repartition('Oursin','fond', nb, rotation, scale_min, scale_max)

    #_______ application couleurs ________#
    ApplyColor("Oursin", colo, 0)


def repartirEtoiles(nb, rotation, scale_min, scale_max, colo):
    if cmds.objExists("EtoileDeMer*"):
        cmds.delete("EtoileDeMer*")
    #-----import du mesh etoiles
    setImport('EtoileDeMer.fbx')

    #----- appel de la fonction de r�partition
    Repartition('EtoileDeMer1','Rochers', nb-2-1, rotation, scale_min, scale_max)
    #Repartition('EtoileDeMer1','Rocher_gros1', 2, rotation, scale_min, scale_max)
    #Repartition('EtoileDeMer1','Rocher_moyen1', 1, rotation, scale_min, scale_max)

    ApplyColor("EtoileDeMer", colo, 0.4)

def repartirCorauxCone(nb, rotation, scale_min, scale_max, colo):
    if cmds.objExists("CorailCone*"):
        cmds.delete("CorailCone*")

    #-----import des mesh coraux cone
    setImport('CorailCone_complexe.fbx')
    setImport('CorailCone_double.fbx')
    setImport('CorailCone_seul.fbx')
    setImport('CorailCone_triple.fbx')

    #----- d�finition du nombre d'instance par type
    if (nb%2 == 0 ): # nb pair
        nbS = nb / 4
        nbD = nb / 4
        nbT = nb / 4
        nbC= nb / 4
    if(nb%2 !=0 ): #nb impair
        nbS = ((nb-1) / 4) +1
        nbD = (nb-1) / 4
        nbT = (nb-1) / 4
        nbC= (nb-1) / 4

    #----- appel de la fonction de r�partition
    grpAnimVague.append(Repartition('CorailCone_complexe','fond', nbC, rotation, scale_min, scale_max))
    grpAnimVague.append(Repartition('CorailCone_seul','fond', nbS, rotation, scale_min, scale_max))
    grpAnimVague.append(Repartition('CorailCone_double','fond', nbD, rotation, scale_min, scale_max))
    grpAnimVague.append(Repartition('CorailCone_triple','fond', nbT, rotation, scale_min, scale_max))


    ApplyColor("CorailCone", colo, 0.2)

def repartirCorauxPhone(nb, rotation, scale_min, scale_max, colo):
    if cmds.objExists("CorailPhone*"):
        cmds.delete("CorailPhone*")
    #-----import des mesh coraux phone
    setImport('CorailPhone_double.fbx')
    setImport('CorailPhone_seul.fbx')
    setImport('CorailPhone_triple.fbx')

    #----- d�finition du nombre d'instance par type
    if (nb%2 == 0 ): # nb pair
        nbS = nb / 3
        nbD = nb / 3
        nbT = nb / 3
    if(nb%2 !=0 ): #nb impair
        nbS = ((nb-1) / 3) +1
        nbD = (nb-1) / 3
        nbT = (nb-1) / 3


    #----- appel de la fonction de r�partition
    grpAnimVague.append(Repartition('CorailPhone_seul','fond', nbS, rotation, scale_min, scale_max))
    grpAnimVague.append(Repartition('CorailPhone_double','fond', nbD, rotation, scale_min, scale_max))
    grpAnimVague.append(Repartition('CorailPhone_triple','fond', nbT, rotation, scale_min, scale_max))

    ApplyColor("CorailPhone", colo, 0.2)

def repartirPoissons(co, colo, ShoalNumber, nbFish, typeFishRadio, espacementFish, scaleFish):
    if (typeFishRadio== 2): # = le poisson long
        setImport("PoissonLong.fbx")
        nomType = "PoissonLong"
    if (typeFishRadio== 1): # = le poisson rong
        setImport("PoissonFleche.fbx")
        nomType = "PoissonFleche"
    
    for i in range(0, ShoalNumber):
        shoal(co, colo, nbFish, espacementFish, scaleFish, nomType)
        co +=1
    return co

def repartirAlgues(nb, rotation, colo):
    gAlgue = dessAlgue(
        cmds.radioButtonGrp(UIembout, q=True, select=True),
        cmds.floatSliderGrp(UIpuissance, q=True, value=True),
        cmds.floatSliderGrp(UItailleMin, q=True, value=True),
        cmds.floatSliderGrp(UItailleMax, q=True, value=True),
        cmds.floatSliderGrp(UIepaisseur, q=True, value=True), 
        cmds.intSliderGrp(UInbBranchesMin, q=True, value=True), 
        cmds.intSliderGrp(UInbBranchesMax, q=True, value=True), 
        cmds.intSliderGrp(UInbSousBranchesMin, q=True, value=True), 
        cmds.intSliderGrp(UInbSousBranchesMax, q=True, value=True), 
        cmds.floatSliderGrp(UIproportionMin, q=True, value=True), 
        cmds.floatSliderGrp(UIproportionMax, q=True, value=True)
    )
    colorierAlgue(gAlgue, colo)

    grpAnimVague.append(Repartition(gAlgue,'fond', nb, rotation, 0.05, 0.05))


#__________________________coloration _______________________________________
def ApplyColor(nom, colo, emission):
    mat = cmds.shadingNode('aiStandardSurface', name=nom+"Mat", asShader=True)
    cmds.setAttr(mat+".baseColor", colo[0],colo[1], colo[2])
    cmds.setAttr(mat+".specularRoughness", 1)
    cmds.setAttr(mat+".emission", emission)
    cmds.setAttr(mat+".emissionColor", colo[0],colo[1], colo[2])
    #attribution rochers
    cmds.select(nom+"*",  hi=True, add=True)
    cmds.hyperShade(assign=mat)

#__________________________clean la scene____________________________________
def clean():
    cmds.file(f=True, new=True)
    count = 0



#__________INTERFACE _________
cmds.window(w=450,title="SeaBed Generator")

form = cmds.formLayout(w=1920,h=1080)

tabs = cmds.tabLayout(borderStyle="none",w=450,h=1000)
cmds.formLayout( form, edit=True, attachForm=((tabs, 'left', 15)) )


#//////////////////////TAB1//////////////#


child1 = cmds.scrollLayout(w=300)

#------Field-----#

cmds.text(label="Generate the field of your seabed.", font='boldLabelFont',h=50,align="center")

field_strenth = cmds.floatSliderGrp(field=True,label="Strenth",minValue=0,maxValue=3,value=1.5,w=400)
field_frequency = cmds.floatSliderGrp(field=True,label="Frequency",minValue=0,maxValue=1,value=0.3,w=400)
field_amplitude = cmds.floatSliderGrp(field=True,label="Amplitude",minValue=0,maxValue=1,value=0.4,w=400)
cmds.separator(h=10, style="none")

cmds.button(label="Choose Color",c="couleurs = Color()",bgc=[0.2,0.2,0.2],w=400)
cmds.button(label="Field",c="Fond(couleurs, cmds.floatSliderGrp(field_strenth,q=True,v=True), cmds.floatSliderGrp(field_frequency,q=True,v=True), cmds.floatSliderGrp(field_amplitude,q=True,v=True))", w=400,h=40,al="right")


#------Rocks-----#

cmds.separator(h=20, style="none")
cmds.separator(h=10,w=400)
cmds.text(label="Place some rocks.", font='boldLabelFont',h=50)

#Sources image a changer
cmds.image(image= pathVignettes+"Rochers.png")
cmds.separator(h=20, style="none")

rock_number = cmds.intSliderGrp(field=True,label="Amount",minValue=0,maxValue=10,value=4,w=400)
rock_min = cmds.floatSliderGrp(field=True,label="Min Scale",minValue=0,maxValue=1,value=1,w=400)
rock_max = cmds.floatSliderGrp(field=True,label="Max Scale",minValue=0,maxValue=1,value=1,w=400)
rock_rotate = cmds.floatSliderGrp(field=True,label="Rotation",minValue=0,maxValue=90,value=0,w=400)

cmds.separator(h=10, style="none")

cmds.button(label="Choose Color",c="couleurs = Color()",bgc=[0.2,0.2,0.2],w=400)
cmds.button(label="Rocks", c="repartirRochers(cmds.intSliderGrp(rock_number, q=True, value=True),cmds.floatSliderGrp(rock_rotate, q=True, value=True),cmds.floatSliderGrp(rock_min, q=True, value=True),cmds.floatSliderGrp(rock_max, q=True, value=True), couleurs)",h=40,w=400)


#------Shells-----#

cmds.separator(h=20, style="none")
cmds.separator(h=10,w=400)
cmds.text(label="Place some shells.", font='boldLabelFont',h=50)

#Sources image a changer
cmds.image(image= pathVignettes + "Coquillage.png")
cmds.separator(h=20, style="none")

shell_number = cmds.intSliderGrp(field=True,label="Amount",minValue=0,maxValue=50,value=15,w=400)
shell_min = cmds.floatSliderGrp(field=True,label="Min Scale",minValue=0,maxValue=2,value=0.7,w=400)
shell_max = cmds.floatSliderGrp(field=True,label="Max Scale",minValue=0,maxValue=2,value=0.9,w=400)
shell_rotate = cmds.floatSliderGrp(field=True,label="Rotation",minValue=0,maxValue=180,value=0,w=400)

cmds.separator(h=10, style="none")

cmds.button(label="Choose Color",c="couleurs = Color()",bgc=[0.2,0.2,0.2],w=400)
cmds.button(label="Shells",c="repartirCoquillages(cmds.intSliderGrp(shell_number, q=True, value=True), cmds.floatSliderGrp(shell_rotate, q=True, value=True),cmds.floatSliderGrp(shell_min, q=True, value=True),cmds.floatSliderGrp(shell_max, q=True, value=True), couleurs)",h=40,w=400)


#------Sea Urchin-----#



cmds.separator(h=20, style="none")
cmds.separator(h=10,w=400)
cmds.text(label="Place some sea urchin.", font='boldLabelFont',h=50)

#Sources image a changer
cmds.image(image= pathVignettes + "Oursin.png")
cmds.separator(h=20, style="none")

urchin_number = cmds.intSliderGrp(field=True,label="Amount",minValue=0,maxValue=50,value=15,w=400)
urchin_min = cmds.floatSliderGrp(field=True,label="Min Scale",minValue=0,maxValue=2,value=0.7,w=400)
urchin_max = cmds.floatSliderGrp(field=True,label="Max Scale",minValue=0,maxValue=2,value=0.9,w=400)
urchin_rotate = cmds.floatSliderGrp(field=True,label="Rotation",minValue=0,maxValue=180,value=0,w=400)

cmds.separator(h=10, style="none")

cmds.button(label="Choose Color",c="couleurs=Color()",bgc=[0.2,0.2,0.2],w=400)
cmds.button(label="Sea Urchin",c="repartirOursins(cmds.intSliderGrp(urchin_number, q=True, value=True),cmds.floatSliderGrp(urchin_rotate, q=True, value=True),cmds.floatSliderGrp(urchin_min, q=True, value=True),cmds.floatSliderGrp(urchin_max, q=True, value=True), couleurs)",h=40,w=400)



cmds.setParent( '..' )




#//////////////////////TAB2//////////////#


child2 = cmds.scrollLayout(w=300)



#------StarFish-----#



cmds.text(label="Place some starfish on the rocks.", font='boldLabelFont',h=50)

#Sources image a changer
cmds.image(image= pathVignettes + "EtoileDeMer.png")
cmds.separator(h=20, style="none")

star_number = cmds.intSliderGrp(field=True,label="Amount",minValue=0,maxValue=70,value=5,w=400)
star_min = cmds.floatSliderGrp(field=True,label="Min Scale",minValue=0,maxValue=2,value=0.9,w=400)
star_max = cmds.floatSliderGrp(field=True,label="Max Scale",minValue=0,maxValue=2,value=1.2,w=400)
star_rotate = cmds.floatSliderGrp(field=True,label="Rotation",minValue=0,maxValue=180,value=0,w=400)
cmds.separator(h=10, style="none")

cmds.button(label="Choose Color",c="couleurs= Color()",bgc=[0.2,0.2,0.2],w=400)
cmds.button(label="Starfish",c="repartirEtoiles(cmds.intSliderGrp(star_number, q=True, value=True),cmds.floatSliderGrp(star_rotate, q=True, value=True),cmds.floatSliderGrp(star_min, q=True, value=True),cmds.floatSliderGrp(star_max, q=True, value=True), couleurs)",h=40,w=400)


#------Coral#1-----#

cmds.separator(h=20, style="none")
cmds.separator(h=10,w=400)
cmds.text(label="Place some Corals.", font='boldLabelFont',h=50)

#Sources image a changer
cmds.image(image= pathVignettes + "Coraux1.png")
cmds.separator(h=20, style="none")

coral_number = cmds.intSliderGrp(field=True,label="Amount",minValue=0,maxValue=20,value=6,w=400)
#coral_density = cmds.intSliderGrp(field=True,label="Density",minValue=0,maxValue=10,value=3,w=400)
coral1_min = cmds.floatSliderGrp(field=True,label="Min Scale",minValue=0,maxValue=1,value=0.7,w=400)
coral1_max = cmds.floatSliderGrp(field=True,label="Max Scale",minValue=0,maxValue=1,value=1,w=400)
coral_rotate = cmds.floatSliderGrp(field=True,label="Rotation",minValue=0,maxValue=180,value=0,w=400)

cmds.separator(h=10, style="none")

cmds.button(label="Choose Color",c="couleurs = Color()",bgc=[0.2,0.2,0.2],w=400)
cmds.button(label="Coral#1",c="repartirCorauxCone(cmds.intSliderGrp(coral_number, q=True, value=True),cmds.floatSliderGrp(coral_rotate, q=True, value=True), cmds.floatSliderGrp(coral1_min, q=True, value=True),cmds.floatSliderGrp(coral1_max, q=True, value=True), couleurs)",h=40,w=400)

#------Coral#2-----#

cmds.separator(h=20, style="none")
cmds.separator(h=10,w=400)
cmds.text(label="Place some Corals.", font='boldLabelFont',h=50)

#Sources image a changer
cmds.image(image= pathVignettes + "Coraux2.png")
cmds.separator(h=20, style="none")

coral2_number = cmds.intSliderGrp(field=True,label="Amount",minValue=0,maxValue=20,value=6,w=400)
#coral2_density = cmds.intSliderGrp(field=True,label="Density",minValue=0,maxValue=10,value=3,w=400)
coral2_min = cmds.floatSliderGrp(field=True,label="Min Scale",minValue=0,maxValue=1,value=0.5,w=400)
coral2_max = cmds.floatSliderGrp(field=True,label="Max Scale",minValue=0,maxValue=1,value=0.8,w=400)
coral2_rotate = cmds.floatSliderGrp(field=True,label="Rotation",minValue=0,maxValue=180,value=0,w=400)

cmds.separator(h=10, style="none")

cmds.button(label="Choose Color",c="couleurs = Color()",bgc=[0.2,0.2,0.2],w=400)
cmds.button(label="Coral#2",c="repartirCorauxPhone(cmds.intSliderGrp(coral2_number, q=True, value=True),cmds.floatSliderGrp(coral2_rotate, q=True, value=True),cmds.floatSliderGrp(coral2_min, q=True, value=True),cmds.floatSliderGrp(coral2_max, q=True, value=True), couleurs)",h=40,w=400)


cmds.setParent( '..' )




#//////////////////////TAB3/////////////////#

child3 = cmds.scrollLayout(w=300)
#cmds.iconTextRadioCollection( "itRadCollection" )


#------Fish-----#
cmds.separator(h=15, style="none")

cmds.text(label="Generate Shoal. ", font='boldLabelFont',h=50)

cmds.separator(h=10, style="none")
cmds.rowColumnLayout(numberOfColumns=2,cw=[(1,200),(2,200)])


typeFishI=cmds.iconTextRadioCollection( 'fishCollection10' ) #il faudrait soit faire sans, donc via une autre
#maniere de mettre en forme les bouttons, soit vérifier si le nom de l'objet existe avec un objExists(fishCollection) ?
fleche=cmds.iconTextRadioButton( st='iconOnly', i1= pathVignettes +'PoissonFleche.png', l='fleche')
long=cmds.iconTextRadioButton( st='iconOnly', i1= pathVignettes+'PoissonLong.png', l='long')

cmds.setParent("..")
cmds.separator(h=20, style="none")

typeFish = cmds.radioButtonGrp(numberOfRadioButtons=2, label='Type of fish', labelArray2=['Arrow One', 'Long One'], select=2)
SliderScaleFishy = cmds.floatSliderGrp(field=True,label="Fish Scale",minValue=0.2,maxValue=1,value=0.5,w=400)
SliderNbFish = cmds.intSliderGrp(field=True,label="Fish per Shoal",minValue=4,maxValue=20,value=6,w=400)
SliderEspaceFish = cmds.floatSliderGrp(field=True,label="Space between Fish",minValue=3,maxValue=6,value=3.5,w=400)
SliderNbShoal = cmds.intSliderGrp(field=True,label="Shoal Amount",minValue=1,maxValue=10,value=3,w=400)

cmds.separator(h=30, style="none")

cmds.button(label="Choose Color",c="couleurs = Color()",bgc=[0.2,0.2,0.2],w=400)

cmds.button(label="Shoal", c="count = repartirPoissons(count, couleurs, cmds.intSliderGrp(SliderNbShoal, q=True, value=True), cmds.intSliderGrp(SliderNbFish, q=True, value=True), cmds.radioButtonGrp(typeFish, q=True, select=True), cmds.floatSliderGrp(SliderEspaceFish, q=True, value=True), cmds.floatSliderGrp(SliderScaleFishy, q=True, value=True))",h=40,w=400)

cmds.separator(h=30, style="none")
cmds.separator(h=10,w=400)




#------Algae-----#

cmds.separator(h=30, style="none")
cmds.rowColumnLayout(numberOfColumns=2,cw=[(1,380),(2,20)])

cmds.text(label="Create your Algae.", font='boldLabelFont',h=20,w=100)
cmds.button(label="i",c="AlgaeExp()",h=20,w=20)
cmds.setParent("..")
cmds.separator(h=20, style="none")

cmds.rowColumnLayout(numberOfColumns=3,cw=[(1,140),(2,120),(3,130)])

#typeEmbout2=cmds.iconTextRadioCollection( 'algaeCollection' )
#cmds.iconTextRadioButton( st='iconOnly', i1='cube.png', l='cube', cl='algaeCollection')
#cmds.iconTextRadioButton( st='iconOnly', i1='sphere.png', l='sphere', cl='algaeCollection')
#cmds.iconTextRadioButton( st='iconOnly', i1='cone.png', l='cone', cl='algaeCollection')

cmds.setParent("..")

UIembout = cmds.radioButtonGrp( label="Type d'embout", labelArray3=['Sphere', 'Cube', 'Cone'], numberOfRadioButtons=3, select=1 )

cmds.rowColumnLayout(numberOfColumns=1)
cmds.separator(h=20, style="none")

UItailleMin = cmds.floatSliderGrp(field=True, label='Min Scale', minValue=0.1, maxValue=1, value=0.7, w=400)
UItailleMax = cmds.floatSliderGrp(field=True, label='Max Scale', minValue=0.1, maxValue=1, value=0.7, w=400)
UIepaisseur = cmds.floatSliderGrp(field=True, label='Width', minValue=0.5, maxValue=2, value=1.0, w=400)
UIpuissance = cmds.floatSliderGrp(field=True, label='Power', minValue=0.2, maxValue=1, value=1, step=.1, w=400)

cmds.separator(h=20, style="none")

UInbBranchesMin = cmds.intSliderGrp(field=True, label='Min branches', minValue=1, maxValue=10, value=2, w=400)
UInbBranchesMax = cmds.intSliderGrp(field=True, label='Max branches', minValue=1, maxValue=10, value=2, w=400)
UInbSousBranchesMin = cmds.intSliderGrp(field=True, label='Min sub branches', minValue=1, maxValue=5, value=2, w=400)
UInbSousBranchesMax = cmds.intSliderGrp(field=True, label='Max sub branches', minValue=1, maxValue=5, value=2, w=400)

cmds.separator(h=20, style="none")

UIproportionMin = cmds.floatSliderGrp(field=True, label='Min starting proportion', minValue=0.2, maxValue=.6, value=.5, step=0.1, w=400)
UIproportionMax = cmds.floatSliderGrp(field=True, label='Max starting proportion', minValue=0.2, maxValue=.6, value=.5, step=0.1, w=400)

cmds.separator(h=20, style="none")

algae_number = cmds.intSliderGrp(field=True,label="Numbers",minValue=0,maxValue=50,value=15,w=400)
algae_rotate = cmds.floatSliderGrp(field=True,label="Rotation",minValue=0,maxValue=180,value=0,w=400)
cmds.separator(h=20, style="none")

cmds.button(label="Choose Color",c="couleurs = Color()",bgc=[0.2,0.2,0.2],w=400)

cmds.button(label="Algae", c="repartirAlgues(cmds.intSliderGrp(algae_number, q=True, value=True),cmds.floatSliderGrp(algae_rotate, q=True, value=True), couleurs)",h=40,w=400)

cmds.setParent( '..' )

cmds.setParent( '..' )

#//////////////////////TAB4//////////////#
child4 = cmds.scrollLayout(w=400)

cmds.separator(h=30, style="none")
cmds.text(label="Animate your scene.", font='boldLabelFont',h=20,w=400)
cmds.separator(h=30, style="none")

vague_amplitude = cmds.floatSliderGrp(field=True, label='Amplitude', minValue=0.001, maxValue=0.10, value=0.01, step=0.001, w=400)
vague_lenteur = cmds.floatSliderGrp(field=True, label='Lenteur', minValue=1.5, maxValue=200, value=100, step=0.5, w=400)

cmds.separator(h=3, style="none")

cmds.button(label="Waves", c="boutonAnimerVagues(grpAnimVague, cmds.floatSliderGrp(vague_amplitude, q=True, value=True), 1.5, cmds.floatSliderGrp(vague_lenteur, q=True, value=True))", bgc=[0.2,0.2,0.2],w=400)

cmds.setParent( '..' )

#//////////////////////TAB5//////////////#
child5 = cmds.scrollLayout(w=400)

cmds.separator(h=30, style="none")
cmds.text(label="Render your scene.", font='boldLabelFont',h=20,w=400)
cmds.separator(h=30, style="none")

cmds.button(label="Light",c="SetupLighting()",bgc=[0.2,0.2,0.2],w=400)
cmds.separator(h=3, style="none")
cmds.button(label="Camera",c="SetupCamera()",bgc=[0.2,0.2,0.2],w=400)
cmds.separator(h=10, style="none")
cmds.button(label="Render",c="RenderView() ",w=400,h=100)



cmds.setParent( '..' )
cmds.setParent( '..' )





def Color():

    couleurEditor=cmds.colorEditor()
    couleur = cmds.colorEditor(q=True, rgb=True)
    R=couleur[0]
    V=couleur[1]
    B=couleur[2]
    return R,V,B

def AlgaeExp():
    cmds.window(h=280,w=560,title="Information Algae settings")
    cmds.rowColumnLayout(h=280,w=560,adjustableColumn=True)

    cmds.separator(h=20, style="none")
    cmds.text(label="Algae's parameters info :", font='boldLabelFont')

    cmds.separator(h=25, style="none")

    cmds.text(label="   - Min / Max scale :",align='left',w=400,font='boldLabelFont')
    cmds.separator(h=3, style="none")
    cmds.text(label="       The minimum and maximum scale of the whole algae. \n       For reference, a scale of 1 is about the same size as the big corals.",align='left',w=400,fn="smallPlainLabelFont")
    cmds.separator(h=15, style="none")

    cmds.text(label="   - Min / Max branches :",align='left',w=400,font='boldLabelFont')
    cmds.separator(h=3, style="none")
    cmds.text(label="       The minimum and maximum amount of main branches around the stem.",align='left',w=400,fn="smallPlainLabelFont")
    cmds.separator(h=15, style="none")

    cmds.text(label="   - Min / Max sub branches :",align='left',w=400,font='boldLabelFont')
    cmds.separator(h=3, style="none")
    cmds.text(label="       The minimum and maximum amount of children branches drawn on the prior branche.",align='left',w=400,fn="smallPlainLabelFont")
    cmds.separator(h=15, style="none")

    cmds.text(label="   - Min / Max starting proportion :",align='left',w=400,font='boldLabelFont')
    cmds.separator(h=3, style="none")
    cmds.text(label="       Where the sub branches start according to the prior branches. \n       For example 0.2% will draw each sub branche up about 2/10 of the length of the prior branche.\n       While 0.5% will draw a branche around the middle of the prior branche.",align='left',w=400,fn="smallPlainLabelFont")
    cmds.showWindow()


def SetupLighting() :

	#creation lumiere ambiante
	mutils.createLocator("aiAreaLight", asLight=True)
	lum1 = cmds.rename("LumiereAmbiante")
	cmds.rotate(-90,0,0)
	cmds.move(0, 17,0)
	cmds.scale(15,15,15)
	cmds.setAttr(lum1+".color", 0, 0.19, 1)
	cmds.setAttr(lum1+".intensity", 79)
	#creation lumiere centrale
	mutils.createLocator("aiAreaLight", asLight=True)
	lum2 = cmds.rename("LumiereCentale")
	cmds.rotate(-205,75, -140)
	cmds.move(5,8,-3)
	cmds.setAttr(lum2+".color", 1, 0.66, 0.44)
	cmds.setAttr(lum2+".intensity", 100)

def SetupCamera() :
	cam = cmds.camera()
	cmds.lookThru(cam[0])
	cmds.setAttr(cam[1]+".renderable", True)
	cmds.setAttr("persp.renderable", False)
	cmds.setAttr("top.renderable", False)
	cmds.setAttr("front.renderable", False)
	cmds.setAttr("side.renderable", False)
	cmds.select(cam[0])
	cmds.rotate(-20.738, 48.547, -0.414)
	cmds.move(24.026, 15.354, 21.047)
	cmds.renderSettings(cam=cam[1])

def RenderView() :
    core.createOptions()
    cmds.arnoldRenderView(mode ="open")
    cmds.arnoldRenderView()

cmds.tabLayout( tabs, edit=True, tabLabel=((child1, "Field / Details"), (child2, "Starfish / Corals"), (child3, "Fish / Algae"), (child4, "Animation"), (child5, "Render")) )
cmds.setParent( '..' )
view=cmds.paneLayout(w=1450,h=1080)
cmds.modelPanel(mbv=0)
cmds.formLayout( form, edit=True, attachForm=((view, 'left', 460)) )



cmds.showWindow()

