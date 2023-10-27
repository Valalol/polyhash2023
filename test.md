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