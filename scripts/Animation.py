# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.internal.common.cmd.base
import math
import random


#_______________________ ANIMATION DEFORMEUR _______________________#

#Fonction qui permet de creer un le deformeur wave avec deux parametres facultatifs ou de changer ces deux parametres si le deformeur existe deja.
def deformation(amplitude, wavelenght, nomDeform ="sineDeform", effet="sine"):
    if (not cmds.objExists(nomDeform)):
        maya.internal.common.cmd.base.executeCommand(effet+'.cmd_create')
        rDeform = cmds.ls(sl=True, fl=True) #on recupere le handle en premier puis le deformer
        cmds.deformer(rDeform[1], e=True, n=nomDeform)
        cmds.move(0, 7, 0, rDeform[0])
        cmds.rotate(0, 0, 180, rDeform[0])
        cmds.scale(1, 1, 1, rDeform[0])
    else:
        print("nomDeformer deja existant")

    cmds.setAttr(nomDeform+".amplitude", amplitude)
    cmds.setAttr(nomDeform+".wavelength", wavelenght)
    cmds.setAttr(nomDeform+".dropoff", 1)
    cmds.setAttr(nomDeform+".lowBound", 0)
    cmds.setAttr(nomDeform+".highBound", 7)
    return nomDeform

#Fonction qui permet d'animer l'offset du deformeur du meme nom, en le liant via une expression au temps.
#Le rapport est divise par un parametre (par default 100) lenteur qui divise le temps par la valeur indiquee.
def animerDeformation(lenteur, nomDeform):
    nom = str(nomDeform) +"_Expression"
    if(not cmds.objExists(nom)):
        cmds.expression(n = nom, s= nomDeform+".offset = time1.outTime/"+str(lenteur))
    else:
        cmds.expression(nom, e=True, s= nomDeform+".offset = time1.outTime/"+str(lenteur))

def boutonAnimerVagues(grpAnimVague, amplitude=0.3, wavelenght=4.3, lenteur=20):
    cmds.select(grpAnimVague)
    rDef = deformation(amplitude, wavelenght)
    animerDeformation(lenteur, rDef)

#_______________________ ANIMATION BOIDS _______________________#
class poissonBoid:
    "Classe de poisson se deplacant de maniere boidienne"
    #VARIABLES DE CLASSE:
    rBoid = "temp" #Reference du mesh (objet maya) dans la scene
    listeBoids = [] #Liste de tous les objets de cette classe

    rayCoh = 15 #Rayon a partir du quel les poissons font la COHESION
    rayAli = 10 #Rayon a partir du quel les poissons font la ALIGNEMENT
    raySep = 5 #Rayon a partir du quel les poissons font la SEPARATION

    vitNag = 0.5 #Vitesse (en unite maya), d'avancement du poisson
    puiCoh = 0.0 #/!\ Laisser a 0 #Puissance d'orientation (% de 0 a 1), vers le centre des voisins
    accCoh = 0.01 #Pourcentage d'augmentation de la puissance d'orientation vers ce centre
    accSep = 0.02 #Pourcentage de reduction de la puissance d'orientation vers ce centre (peut aller dans le negatif)
    accAli = 10 #Angle de rotation pour l'alignement d'orientation

    def __init__(self, nom="boid"):
        self.rBoid = cmds.polyCone(n=nom, axis=(0,1,0))
        self.listeBoids.append(self.rBoid)

    #(FONCTION METHODES JSP MATHS)
    def getPos(self, obj): # Recuperer la position d'un objet
        return (cmds.xform(obj, q=True, t=True, ws=True))
    def getDis(self, pA, pB): # Recuperer la distance entre deux positions
        dis = math.sqrt( abs( pow((pB[0]-pA[0]), 2) + pow((pB[1]-pA[1]), 2) + pow((pB[2]-pA[2]), 2) ) )
        return dis
    def getPosMoyenne(self, listePos):
        pMoyX = 0
        pMoyY = 0
        pMoyZ = 0
        pond = 0
        for p in listePos:
            pMoyX += p[0]
            pMoyY += p[1]
            pMoyZ += p[2]
            pond += 1
        if (pond > 0):
            pMoyX /= pond
            pMoyY /= pond
            pMoyZ /= pond
            return [pMoyX, pMoyY, pMoyZ]
        else:
            return None
    def getVecNorm(self, pA, pB): # Recuperer la vecteur normalise entre deux positions
        vecX = (pB[0] - pA[0])
        vecY = (pB[1] - pA[1])
        vecZ = (pB[2] - pA[2])
        dis = self.getDis(pA, pB)
        vecX /= dis
        vecY /= dis
        vecZ /= dis
        return(vecX, vecY, vecZ)
    def ralentQuad(self, dis, vit, disTol):# Courbes de ralentissement et d'acceleration selon la distance
        return (dis/disTol) * (dis/disTol-2) + vit
    def accelQuad(self, dis, vit, disTol):
        return (dis/disTol) * (dis/disTol)
    def getAngle(self, obj):
        return cmds.xform(obj, q=True, rotation=True)
    def convVecToAng(self, vecA):
        # degX = (math.atan2(math.sqrt(vecA[1]^2+vecA[2]^2),vecA[0])*180/math.pi)
        # degY = (math.atan2(math.sqrt(vecA[2]^2+vecA[0]^2),vecA[1])*180/math.pi)
        # degZ = (math.atan2(math.sqrt(vecA[0]^2+vecA[1]^2),vecA[2])*180/math.pi)
        # degX = math.atan2(vecA[0], vecB[0])*180/math.pi
        # degY = math.atan2(vecA[1], vecB[1])*180/math.pi
        # degZ = math.atan2(vecA[2], vecB[2])*180/math.pi
        degX = math.atan2(vecA[1], vecA[2])*180/math.pi
        degY = math.atan2(vecA[2], vecA[0])*180/math.pi
        degZ = math.atan2(vecA[0], vecA[1])*180/math.pi

        return [degX, degY, -degZ]


    #(METHODES UTILES)
    def getVoisins(self, rayon):
        voisins=[]
        for b in self.listeBoids:
            dis = self.getDis( self.getPos(self.rBoid), self.getPos(b))
            if (dis == 0):
                pass
            elif(dis < rayon):
                voisins.append(b)
        return voisins

    def placer(self, tx, ty, tz, rx, ry, rz):
        cmds.move(tx, ty, tz, self.rBoid, a=True)
        cmds.rotate(rx, ry, rz, self.rBoid, a=True)

    # (MOUVEMENT BASE)
    def nager(self):
        cmds.move(0, self.vitNag, 0, self.rBoid, r=True, os=True)

    # (BOID:COHESION)
    def boidCohSep(self):#, pA, pB, dis, vecNormAB, vit=1.0, disTol=30.0):
        #VARIABLES
        voisins = self.getVoisins(self.rayCoh)
        nomLoc = "groupeCohesion_" +self.rBoid[0]
        nomCon = "contrainteCohesion_" +self.rBoid[0]
        
        #VOISINS
        if (len(voisins) > 0):
            posVoisins = []
            for v in voisins:
                posVoisins.append(self.getPos(v))
            posMoy = self.getPosMoyenne(posVoisins)
            
            #LOCATOR
            if (not cmds.objExists(nomLoc)):
                cmds.spaceLocator(n= nomLoc)
            cmds.move(posMoy[0], posMoy[1], posMoy[2], nomLoc)
            cmds.setKeyframe(nomLoc, at=["tx", "ty", "tz"])

            #CONTRAINTE
            if (not cmds.objExists(nomCon)):
                cmds.aimConstraint(nomLoc, self.rBoid, aimVector=(0,1,0))
            
            #ORIENTATION
            if ( self.getDis( self.getPos(self.rBoid), self.getPos(nomLoc)) < self.raySep):
                self.puiCoh -= self.accCoh
            else:
                self.puiCoh += self.accSep
            cmds.setAttr(self.rBoid[0] +".blendAim1", self.puiCoh)
            cmds.setKeyframe(self.rBoid, at=".blendAim1")
        #SEUL
        else:
            self.puiCoh = 0
            if (cmds.objExists(nomLoc)):
                cmds.delete(nomLoc)
            if (cmds.objExists(nomCon)):
                cmds.delete(nomCon)



    # (BOID:ALIGNEMENT)
    def boidAli(self):
        voisins = self.getVoisins(self.rayAli)
        if (len(voisins) > 0):
            oriVoisins = []
            for v in voisins:
                oriVoisins.append(self.getAngle(v))
            oriMoy = self.getPosMoyenne(oriVoisins)

            oriIni = self.getAngle(self.rBoid)
            for r in range(0, len(oriIni)):
                if oriIni[r]+self.accAli < oriMoy[r]:
                    oriIni[r] += self.accAli
                elif oriIni[r] < oriMoy[r]:
                    oriIni[r] += oriMoy[r]-oriIni[r]
                elif oriIni[r]-self.accAli > oriMoy[r]:
                    oriIni[r] -= self.accAli
                elif oriIni[r] > oriMoy[r]:
                    oriIni[r] -= oriIni[r]-oriMoy[r]
                else:
                    pass
            cmds.rotate(oriIni[0], oriIni[1], oriIni[2], self.rBoid, a=True)

    # (LANCER SIMULATION)
    def simuler(self):
        self.nager()
        self.boidAli()
        self.boidCohSep()


#--------------------------------------------------Scene--------------------------------------------------
cmds.file(new=True, f=True)

def creerPoissons(nb):
    p = []
    for i in range(0, nb):
        p.append( poissonBoid("petitPoisson_" +str(i)) )
        poissonBoid.placer(p[i], random.uniform(-10,10), random.uniform(-10,10), random.uniform(-10,10), 0, 0, 0)
    return p

def lancerSimulation(rPoissons, duree):
    for i in range(1, duree+1):
        cmds.currentTime(i)
        for p in rPoissons:
            cmds.setKeyframe(p.rBoid, at=["tx", "ty", "tz", "rx", "ry", "rz"], t=i)
            poissonBoid.simuler(p)

# cmds.autoKeyframe(state=True)
# rPoissons = creerPoissons(20)
# lancerSimulation(rPoissons, 50)

# p1 = poissonBoid("poissonTest")
# p2 = poissonBoid("poissonTesteuuuuh")
# poissonBoid.simuler(p1)