# SeaBedGenerator
ATI - L3 - Projet en groupe sur Python d'une génération de fonds marins interactif

Bonjour ! 

Pour faire fonctionner ce générateur il faut : 
1 : Copier-coller tout les scripts (py) dans ce dossier C:\Users\nom_utilisateur\Documents\maya\2018\scripts
2 : Mettre les modèles 3D dans un dossier et changer le path (ligne 26) dans le code main.py avec le chemin 
jusqu'au dossier regroupant les fbx
3: Changer les chemins dans l'interface également en pointant le dossier de vignettes (main.py, ligne 24, 407 et 408)
4 : ouvrir tout les scripts dans l'editeur Maya (ou autre) 
5: Exécuter le code imports.py -> sol.py -> fish.py -> Algues.py -> RepartitionCode.py -> Animation.py (ça permet de les compiler et 
de pas avoir d'erreur quand on va executer le main.py)  
6: executer le main.py (et ça fonctionne!)



Explications : 
/!\ imports.py = la fonction qui permet d'importer tout les assets /!\ plus d'actualité car bug donc je l'ai directement intégré dans le main
Sol.py = la fonction créant le sol 
Algues.py = fonction générant les algues 
fish.py = fonction générant les bancs de poissons 
ReparitionCode.py = fonction générique qui est utilisée pour répartir les assets 
main.py = code principal avec l'interface et les differentes fonctions regroupant pour chaque assets l'import et la répartition des assets et les fonctions de rendus
