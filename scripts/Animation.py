# -*- coding: utf-8 -*-
import math
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
class poissonBoid:
    "Classe de poisson se deplacant de maniere boidienne"
    #Variables de classe:
    rBoid = "temp"
    nom = "temp"
    raySep = 5.0
    rayAli = 10.0
    rayCoh = 15.0
    vitesse = 0.5
    listeBoids = []

    def __init__(self, nom="boid"):
        self.nom = nom
        self.rBoid = cmds.polyCone(n=self.nom, axis=(1,0,0))
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

    def getAngle(self):
        print("angle de '{}' = ".format(self.rBoid))
        print(cmds.xform(self.rBoid, q=True, rotation=True))

    #(METHODES UTILES)
    def placer(self, tx, ty, tz, rx, ry, rz):
        cmds.move(tx, ty, tz, self.rBoid, a=True)
        cmds.rotate(rx, ry, rz, self.rBoid)
    
    def tourner(self, cible):
        pass

    def getVoisins(self, rayon):
        voisins=[]
        for b in self.listeBoids:
            dis = self.getDis( self.getPos(self.rBoid), self.getPos(b))
            if (dis == 0):
                pass
            elif(dis < rayon):
                voisins.append(b)
        return voisins

    # (MOUVEMENT BASE)
    def nager(self):
        cmds.move(self.vitesse, 0,0, self.rBoid, r=True)

    # (BOID:SEPARATION) 
    def boidSep(self, pA, pB, dis, vecNormAB, vit=1.0, disTol=10.0):
        if(dis < disTol):
            courbe = self.ralentQuad(dis, vit, disTol)
            cmds.move(
                -vecNormAB[0]*courbe, 
                -vecNormAB[1]*courbe, 
                -vecNormAB[2]*courbe, 
                self.rBoid, r=True)
            print("dirAB = " +str(vecNormAB))
        else:
            print("trop loin")

    # (BOID:COHESION)
    def boidCoh(self):#, pA, pB, dis, vecNormAB, vit=1.0, disTol=30.0):
        voisins = self.getVoisins(self.rayCoh)
        posVoisins = []
        for v in voisins:
            posVoisins.append(self.getPos(v))
        posMoy = self.getPosMoyenne(posVoisins)

        # if(dis < disTol):
        #     courbe = self.ralentQuad(dis, vit, disTol)
        #     cmds.move(
        #         vecNormAB[0]*courbe, 
        #         vecNormAB[1]*courbe, 
        #         vecNormAB[2]*courbe, 
        #         self.rBoid, r=True)
        #     print("courbe = " +str(courbe))
        #     print("dis = " +str(dis))

    # (LANCER SIMULATION)
    def simuler(self, duree):
        duree = int(duree)
        for i in range(1, duree+1):
            #cmds.currentTime(i)
            cmds.setKeyframe(self.rBoid, at=["tx", "ty", "tz", "rx", "ry", "rz"], t=i)


            self.nager()
            self.boidCoh()
            # pA = getPos(sujet)
            # pB = getPos(proche) 
            # dis = getDis(pA, pB)
            # vecNormAB = getVecNorm(pA, pB)
            #boidSep(sujet, proche, pA, pB, dis, vecNormAB)
            #boidCoh(sujet, proche, pA, pB, dis, vecNormAB)


#--------------------------------------------------Scene--------------------------------------------------
cmds.file(new=True, f=True)


p1 = poissonBoid("petitPoisson")
p2 = poissonBoid()
p3 = poissonBoid()

cmds.rotate(45,10,80, p1.rBoid)
poissonBoid.placer(p2, 4, 0, -2, 0, 0, 0)
poissonBoid.placer(p3, 6, 0, -4, 0, 0, 0)
poissonBoid.getAngle(p1)
poissonBoid.simuler(p1, 120)
