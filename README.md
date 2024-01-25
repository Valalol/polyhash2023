# Projet Poly#

## Présentation du projet

La demande de bien a explosé, des nouveaux moyens de transport sont nécessaires, la plus grande corpo arasaka cherche à trouver un nouveaux moyen de délivrer le plus de bien, le plus vite et le moins cher possible.

La réponse: des **cyber-drones**.

Vous êtes chargé d’armer le cerveau de ce réseau de drônes d’une **intelligence high-tech**.


## Présentation du projet

Projet basé sur le problème de qualification du google Hash Code de 2016.

En partant d'un ensemble de drones, d'une liste de commandes et de la disponibilité des produits dans les entrepôts, planifier les opérations des drones de sorte que les commandes soient complétées le plus rapidement possible.

## Présentation de l'équipe

- Esnault Valentin valentin.esnault@etu.univ-nantes.fr
- Tchernychev Maxime maxime.tchernychev@etu.univ-nantes.fr
- Roué Robinson robinson.roue@etu.univ-nantes.fr
- Klein Nael nael.klein@etu.univ-nantes.fr

## Comment télécharger le projet

Il faut soit le télécharger à l'adresse suivante ([lien de téléchargement](https://gitlab.univ-nantes.fr/E218577J/polyhash2023/-/archive/main/polyhash2023-main.zip)), soit cloner le projet avec la commande suivante :

```bash
git clone https://gitlab.univ-nantes.fr/E218577J/polyhash2023.git
```

## Comment lancer le projet

```
python polyhash.py <fichier d'entrée> <fichier de sortie>
```

## Organisation du code

- `polyhash.py` : Fichier principal, permet de lancer le programme en précisant le fichier d'entrée et le fichier de sortie.
- `polyparser.py` : Fichier contenant la fonction permettant de parser le fichier d'entrée et de renvoyer un tuple contenant toutes les informations contenus dans le fichier d'entrée.
- `mesures_temps.py` : Fichier contenant le décorateur permettant de mesurer le temps d'exécution d'une fonction.
- `utils.py` : Fichier contenant les fonctions utilitaires telles que `calculate_weigth()`, `check_b_in_a()`, `dict_add()` et `dict_subtract()`.
- `polysolver.py` : Fichier contenant la fonction `solve()` redirigeant vers les différentes stratégies de résolution ainsi que la fonction `save_solution()`
- `/strategies` : Dossier contenant les différentes stratégies de résolution.
- `/challenges` : Dossier contenant les différents challenges.
- `/Doc` : Dossier contenant plusieurs fichiers pense-bête et des pistes de reflexion.

# Fonctionnement de la stratégie
- On trie trie les commandes par nombre d'item puis par distance à l'entrepôt de départ
- On séléctionne la première commande
- On sélectionne le premier item de la commande
- On trouve l'entrepôt le plus proche qui contient cet item puis en restant à cet entrepôt, elle va prendre le plus d'items possibles concernant la commande actuelle
- si le drone arrive à prendre tous les items permettant de finir la commande, il va passer à la commande suivante et prendre des items en plus et ce jusqu'à ce qu'il n'arrive plus à compléter la commande actuelle ou qu'il n'ai plus la place de transporter plus d'items
- une fois qu'il a été prendre ses items, il va les déposer aux commandes pour lesquelles les items ont été pris
- une fois qu'il a tout livré, il repart à 0 et recommence au début

## Résultats obtenus

| Challenge | Score | Classement | Temps d'execution | RAM utilisée |
| :---------: | :---------: | :---------: | :---------: | :---------: |
| A | 238 | Top 1 ex equo | 0.002s | 23.0 MiB |
| B | 101373 | Top 9 | 1.750s | 27.8 MiB |
| C | 95310 | Top 12 | 2.145s | 27.2 MiB |
| D | 74249 | Top 7 | 1.423s | 26.0 MiB |
| Total | 271170 | Top 10 |

## Pistes d'amélioration
Il serait probablement possible de permettre aux drones de charger les produits des commandes sans forcément les faire dans l'ordre mais plutot de prendre tous les produits utiles sur les prochaines commandes.

Cela demmanderait un peu de restructuration pour pouvoir passer de commande en commande tout en revenant sur celles qui n'ont pas pu être complétées pour les finir grace aux drones suivants.