# INCONTOURNABLES:
a=(Xa-Xb)

b=(Ya-Yb)

calcul de distance euclidienne (a^2+b^2)^(1/2)

ou de distance non euclidienne |a+b|

# Étude de la position des commandes
étude de la sparsité des commandes

si les commande sont très sparses alors mieux vaux ne pas faire de cluster et fonctionner avec un quadrillage.

# Étude des commandes:
on prend une partie des commandes:

on calcule le nombre d'item moyen par commande

on calcule l'écart type de nombre d'item par commande

# Conclusion
si l'écart type est grand mieux vaux vérifier le nombre d'item de chaque commande lors de l'évaluation de l'intérêt d'une zone

sinon mieux vaux prendre la valeur moyenne multipliée par le nombre de commande pour obtenir l'interet d'une zone liée aux commandes

# Étude des entrepots:
on prend une partie des entrepots:

on calcule le nombre d'item moyen par entrepot

on calcule l'écart type de nombre d'item par entrepot

# Quadrillage de la map:
quadriller la map en sous map dont on définis un intéret en fonction de la densité des livraison/entrepot -> vérification que les entrepots possède les items nécéssaires.
calcul:

mieux vaux + d'entrepots et peux de commande que peu d'entrepots et plein de commandes.
minimum 1 entrepot + 1 livraison sinon pas de points

chaque entrepots donne 10 points

chaque commande donne 5 points

quadriller la map en sous zones pour définir les zones ou les drones doivent travailler : chaque drone à un bonus de *points* à travailler dans sa zone

## Clusterise de données:

trouver n centre de cluster de livraison/entrepots
faire le même raisonnement de calcul d'interêt que avec un quadrillage

## Dans les "zones":

on enregistre les commandes dans cette zone dans une liste à part

on enregistre les entrepots dans cette zone dans une liste à part

il faudrait trier les entrepots afin de trouver facilement lequel est le plus proche d'un point à un moment donné

soit on procède à un sous-quadrillage, soit on les tries en fonction de leurs coordonnée y ou x ou du gradient x/y

ou on les tries en fonction de leurs nombre d'item ?

# Comment le drone choisis son itinéraire:
ce que les entrepots possèdent dans leur zone

la distance des commandes à lendroit ou il sera et à l'entrepot (l'importance de la distance à l'entrepot varie en fonction de combien d'objets il lui reste)

le nombre d'items par commande

# notes intéressantes sur le sujet
les drones commencent tous du point 0,0

# Ce qui pourrait être le plus efficace en fonction du sujet
~{prendre/deposer différents items demande plusieurs actions : il faut essayer de transporter 1 type de produit dans un drone}

~{1 drone pourrait faire plusieurs commande d'un seul produit mais attention (il ne peut pas faire une partie de la commande d'un produit  --> 1 type de produit doit etre déposé en entier) ((l'ecxédant ira dans le prochain dépot ou alors il y aurait le nombre exact d'items))}

en général on a beaucoup de produit différents et les commandes contiennent des produits différents à l'unité

on peut envoyer tous les drones prendre un maximum de produits différents dans une zone avec beaucoup d'entrepots et de commande mais pas trop loin du départ et les faire avancer par nuée pour faire un max de commandes au début

prendre le bon nombre d'objets différentspour pas que ca prenne trop de tours
(essayer de prendre des items lourds avec des items légers et des moyens entre eux)

# Le plus efficace au niveau des commandes 
les faire le plus vite possible (on gagne des points en fonction du tour avant la fin)

on regarde une grande zone avec le plus de potentiel (entrepot + commandes / offre + demande), dans cette zonne on regarde une petite zone dans laquelle on va avoir le plus d'offre + demande complètes (commande pouvant etre fait avec produit a proximité) puis en fonction des produit qu'il restent dans les drones et des zones alentours chercher les meilleurs ratios offre + demande

avec le déplacement en nuée, on peut tenter de faire un maximum de commandes très vite
