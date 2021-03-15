import maya.cmds as cmds
import random as rand

#clear scenes
cmds.file(f=True, new=True)

path= 'C:/Users/Administrateur/Desktop/Cours/Python/Projet/Models/' #chemins jusqu'au FBX #cmds.internalVar(upd=True)
#print(path) #C:/Users/Administrateur/Documents/maya/2018/prefs/

#__________imports_________   #mettre les bons chemins
#param = choix des assets qu'on va devoir importer / typeAsset = 1 (=poisson)  typeAsset = 2 (=coraux)  typeAsset = 3 (=etoile) typeAsset = 4 (=rocher)
def setImport(typeAsset):
    if (typeAsset == 1): #poisson
        #________chemins d'import poisson_________
        if (cmds.radioButtonGrp(typeFish, q=True, select=True) == 1): # = le poisson long
            setImportPath = path+'Fish_V1.fbx'
        if (cmds.radioButtonGrp(typeFish, q=True, select=True) == 2): # = le poisson rong
            setImportPath = path+'Fish_V2.fbx'
        #____ commande qui importe les fichiers
        cmds.file(setImportPath, i=True, mergeNamespacesOnClash=True, namespace=':')

    if (typeAsset == 2): #coraux
        #________chemins d'import coraux_________
        if (cmds.radioButtonGrp(typeCoraux, q=True, select=True) == 1):
            setImportPath = path+'Corail1_V1.fbx'
            setImportPath2 = path+'Corail1_V2.fbx'
            setImportPath3 = path+'Corail1_V3.fbx'
        if (cmds.radioButtonGrp(typeCoraux, q=True, select=True) == 2):
            setImportPath = path+'Corail2_V1.fbx'
            setImportPath2 = path+'Corail2_V2.fbx'
            setImportPath3 = path+'Corail2_V3.fbx'

        #____ commande qui importe les fichiers
        cmds.file(setImportPath, i=True, mergeNamespacesOnClash=True, namespace=':')
        cmds.file(setImportPath2, i=True, mergeNamespacesOnClash=True, namespace=':')
        cmds.file(setImportPath3, i=True, mergeNamespacesOnClash=True, namespace=':')

    if (typeAsset == 3): #etoile
        #________chemin d'import etoile_________
        setImportPath = path+'Etoile.fbx'

        #____ commande qui importe les fichiers
        cmds.file(setImportPath, i=True, mergeNamespacesOnClash=True, namespace=':')

    if (typeAsset == 4): #rocher
        #________chemin d'import rocher_________
        setImportPath = path+'Rock1.fbx'
        setImportPath2 = path+'Rock2.fbx'
        setImportPath3 = path+'Rock3.fbx'
        setImportPath4 = path+'Rock4.fbx'
        #____ commande qui importe les fichiers
        cmds.file(setImportPath, i=True, mergeNamespacesOnClash=True, namespace=':')
        cmds.file(setImportPath2, i=True, mergeNamespacesOnClash=True, namespace=':')
        cmds.file(setImportPath3, i=True, mergeNamespacesOnClash=True, namespace=':')
        cmds.file(setImportPath4, i=True, mergeNamespacesOnClash=True, namespace=':')

def fish():
    setImport(1)
def coraux():
    setImport(2)
def etoile():
    setImport(3)
def rocher():
    setImport(4)



#_________INTERFACE_____________
# cmds.window(title="Test des imports")
# cmds.columnLayout()
# typeFish = cmds.radioButtonGrp(numberOfRadioButtons=2, label='Type of fish', labelArray2=['Long One', 'Round One'] )
# cmds.button(label="import fish", c="fish()") #fonction de repartition & instance
# typeCoraux = cmds.radioButtonGrp(numberOfRadioButtons=2, label='Type Coraux', labelArray2=['Rond', 'Vague'] )
# cmds.button(label="import coraux", c="coraux()")#fonction de repartition & instance
# cmds.button(label="import etoile", c="etoile()") #fonction de repartition & instance
# cmds.button(label="import rochers", c="rocher()") #fonction de repartition & instance
# cmds.showWindow()
