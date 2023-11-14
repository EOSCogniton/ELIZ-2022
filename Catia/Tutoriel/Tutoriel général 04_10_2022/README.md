Tutoriel CATIA pour 1As - n°1
v1.3 du 04/10/2022 - GLR




Quelques conseils [Importants !] : 
A LIRE AU PREALABLE
- les plans et les droites sont vos amis, à utiliser sans modération ! (Dans la limite du raisonnable bien sûr).
- Une fois utilisés, certains plans, repères et axes ne seront plus utiles. Faire clic droit > Cacher/afficher   pour modifier leur état d'affichage. Dans l'atelier Assembly Design, un bouton avec une icône similaire permetd'afficher tout ce qui est masqué.
- Dans l'arborescence, on s'y perd vite ! Pour y remédier, régulièrement faire clic droit > propriétés, et renommer les différents éléments dans l'arbre.
- Lors de la réalisation du tutoriel, mettez-vous en équipes de deux (avec deux pc et deux Catia ouverts) pour travailler, vous pourrez ainsi vous entraider.
- Ne pas utiliser de caractères acentués, de caractères spéciaux dans les noms de pièces et fichiers. NE PAS UTILISER NON PLUS D'ESPACE. Utiliser plutôt « _ »
A LIRE PENDANT
- Toujours placer les éléments qui servent de référence en tête de l'arbre (sinon les modifier risque de tout faire perdre)
- Pour éditer une pièce, il y a deux possibilités : ou bien on l'ouvre toute seule dans une fenêtre, ce qui implique de faire une définition parfaite et indépendante de toute autre pièce, ou bien on se met dans l'assemblage qui la contient, et on se met "dans le contexte" de la pièce, c'est-à-dire en double-cliquant sur la pièce dans l'arborescence de l'assemblage. Cela va permettre d'éditer la pièce normalement comme en ouverture seule, mais cela donne accès à des interactions avec d'autres pièces et assemblages (exemple : opérations booléennes), appelées références externes. C'est un outil TRES puissant, qui permet de faire des choses qui sont impossibles autrement. Les références externes impliquent en revanche une certaine complexité : "With great power comes great responsibility", et il faut savoir ce que l'on fait.
- Lorsque l'on veut se mettre dans le contexte d'une pièce, il faut double-cliquer sur la partie la plus basse de l'arborescence de cette pièce, sinon le resque est de se retrouver dans le mauvais atelier.
- Pour une pièce simple et sans relation géométrique complexe avec d'autres pièces, TOUJOURS faire la conception en dehors d'un assemblage, puis venir insérer la pièce dans l'assemblage voulu à la fin. C'est systématiquement plus simple.
- Dans la mesure du possible, travailler au maximum sur les pièces en dehors d'un contexte d'assemblage.
- Bien vérifier sur quel objet s’accroche une contrainte lorsqu’on travaille en contexte d’assemblage On peut générer des références externes non souhaitées si la contrainte s’accroche à la géométrie d’une pièce voisine. L’erreur la plus courante est d’accrocher des contraintes aux plans du repère absolu ou au repère crée dans une autre pièce. Ce problème va être partiellement réglé par le réglage effectué à l'étape 0. Il est fondamental et tout membre de l'EPSA doit avoir fait ce réglage.
- Une pièce rouge ne veut pas forcément dire qu'il y a une erreur. Cela peut dire que son affichage n'est pas actualisé et qu'il faut le mettre à jour. Cela peut être fait par l'icône de vortex bleu et vert, ou clic droit > Mettre à jour.
- Si la couleur persiste, il y a une erreur de définition de la pièce. Il faut l'ouvrir, commencer par examiner les messages d'erreur, les références externes et remonter au problème. Une esquisse mal définie aura des traits blancs (changements libres de géométrie, esquisse insuffisamment contrainte), voire pire, violets (esquisse sur-contrainte). Il faut supprimer des contraintes et en modifier jusqu'à obtenir une esquisse toute verte. 
- Il est parfois plus simple de recommencer de zéro une esquisse (simple) que de la réparer.
- Dans Outils > Options, on peut trouver de nombreux éléments très utiles. On peut zoomer/dézoomer dans l'arbre de la même manière que dans l'environnement 3D.




Navigation : 
Préambule : par la suite, on appelle clic molette le fait d'appuyer sur sa molette, qui constitue un troisième bouton cliquable dans 99% des souris.
- Clic molette maintenu pour décaller la vision de la caméra de gauche à droite et de haut en bas
- Clic molette maintenu suivi de clic droit maintenu pour tourner autour de la pièce
- Clic molette maintenu suivi de clic droit très bref + mouvements de souris de haut en bas pour zoomer/dézoomer

Procédure à suivre :

********** étape 0 : mise en place **********

- Ouvrir Catia V5, faire Outils > Options
- Dans général, mettre le délais d'enregistrement automatique sur 10 minutes.
- Dans Infrastructure > Infrastructure Part (symbole d'engrenage après avoir déroulé le menu infrastructure), cocher : 
	- Garder le lien avec l'objet sélectionné ("Keep link with selected object")
	- Restreindre la sélection externe avec lien aux éléùents publiés ("Only use Published Elements for external selection keeping link")
- Concernant les couleurs, il est préférable de laisser les couleurs par défaut, afin que tout le monde se comprenne.
- Faire les réglages d'optimisation suivants : https://www.youtube.com/watch?v=I8bL5fbv5sI

********** étape 1 : création des filaires **********
Dans l'ordre qui suit :
FILAIRE TUBES
- Faire Insertion > Nouvelle pièce (deux fois)
- Faire Insertion > Nouveau produit (trois fois)
- Renommer les pièces "filaire tubes" et "filaire chapes"
- Renommer les produits (assemblages) "tubes", chapes" et "gabarits"
- Se mettre dans le contexte du filaire tubes (double-clic dans l'arborescence)
- Dans le menu démarer, se mettre dans l'atelier Conception Mécanique > Wireframe and Surface Design
- Par la suite, l'ajout d'éléments de cet atelier peut être fait via les icône disponibles, ou Insertion > élément filaire > ...
- Créer trois points, aux coordonnées (0,0,0) , (400,0,0), (400,200,0)
- Les relier par deux droites
- A partir de l'icône plan, créer un plan qui passe par l'axe z, et qui forme un angle de 10° avec le plan yz. Le renommer plan chapes parallele.
- Pour chacune des droites, créer deux plans normaux à ces droites, aux deux points d'extrêmités de ces droites (astuce : pour chaque création, sélectionner la droite, le point en maintenant la touche ctrl, puis cliquer sur l'icône plan. Cela va automatiquement mettre le pla normal à la droite).
- Le fichier filaire tubes est maintenant réalisé, publier les différents plans et axes qui le composent, en se mettant dans le contexte de l'assemblage COMPLET, par le menu Outils > Publication
FILAIRE CHAPES
- Se mettre dans le contexte du filaire chapes
- A partir de l'icône point, créer un point sur la droite qui est selon l'axe x (grâce au fait de l'avoir publiée, on peut interragir avec), à une distance de 200 de l'origine.
- Créer un plan parallèle au plan de chapes qui passe par le point nouvellement créé
- Sélectionner ce plan, etinsérer une intersection avec la deuxième droite (la plus longue), qui va créer un point.
- Sélectionner ce plan, créer un point dessus en sélectionnant le point sur la droite comme origine, et appliquer un décallage horizontal de 40mm, et vertical de 0mm [Ne pas cliquer ailleurs que dans la fenêtre avant d'avoir sélectionné "ok"].
- Sélectionner de nouveau le plan, créer un point dessus en sélectionnant le point sur la deuxième droite comme origine, et appliquer un décallage horizontal de 40mm, et vertical de 0mm.



- Publier également les éléments du filaire chapes.
- enregistrer

********** étape 2 : création des tubes **********
- Se mettre dans le contexte des 
- Réaliser l'esquisse du premier tube sur le plan yz, avec deux cecles concentriques de 28 et 30 mm de diamètre.
- Extruder le premier tube jusqu'au plan de l'extrêmité du filaire, en cliquant ok sur la boîte de dialogue prévenant de la création d'un nouveau volume.
- Cacher ce premier tube, et réaliser la même séquence d'opérations pour le second, cette fois-ci avec des diamètres de 18.5 et 20mm.
- Cacher tous les éléments non utilisés pour la suite (notamment le filaire tubes), de manière à obtenir ceci :
[2022-10-04 23_50_24-Window.jpg]
- publier le corps principal du tube bas (depuis l'assemblage GLOBAL)
- En se mettant dans le contexte du tube haut, faire Insertion > Opérations booléennes > Enlever, et enlever le tube bas au tube haut, faire ok.
- faire Insertion > Opérations booléennes > Relimitation partielle, sélectionner une face du petit morceau de tube à enlever, faire ok.
- enregistrer

********** étape 3 : création de la chape bas **********
- Se mettre dans le contexte du produit chapes. Faire Insertion > nouvelle pièce
- faire Clic droit > Propriétés, renommer la nouvelle pièce en "chape bas"
- Se mettre dans le contexte de la pièce
- Sélectionner le plan de chape, créer une esquisse dessus
- Sélectionner le point décallé de 40mm de l'axe, faire Insertion > Géométrie 3D > Projection des éléments 3D
- Créer une droite pointillée entre le point sur l'axe et le point suivant.
- Faire Clic droit sur la pièce > chape bas > Ouvrir dans une nouvelle fenêtre
- enregistrer



********** étape 4 : création de la chape haut **********
- Idem
- enregistrer

