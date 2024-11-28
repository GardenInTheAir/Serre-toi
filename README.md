# Serre-toi

## Description
Ceci est un site web de réservation d'activité pour un club étudiant s'occupant des plantes. Le site web a été développé initialement dans le cadre du cours MEC1315 (Technologies informationnelles en ingénierie) à l'université Polytechnique de Montréal. Le club et les activités en questions ne sont pas réels. Ils servent comme outils seulement pour représenter les fonctionnements des différents sections de cette application web.
Le site web est encore sous construction. Le deployement actuel sert comme experimentation pour tester le fonctionnement et partager le site avec plus de gens pour avoir plus de retours pour améliorer encore plus le fonctionnement.

## Participants
Ce site web a été initialement développé en collaboration avec deux autres collègues (Gagnon-Lafrenais, N. et Abderahim, M.). On a développé le site web ensemble en utilisant `PHP`. Pourtant, j'ai voulu lui apporter plus de modifications et expérimenter encore plus. Donc, j'ai décidé de le maintenir.

## Modifications apportés
1. Au lieu de `PHP`, la langage de programmation utilisée maintenant est `python` parce que je suis plus à l'aise avec celle-ci.
2. Au lieu de la base de données de l'université Polytechnique, le site web utilise maintenant un serverless database de DataStax Astra. Après un bout de temps, la base de données entre en hibernation dû au non usage fréquent. Donc, j'essaie de garder un accès fréquent au site web pour empécher l'hibernation de la base de données.
3. Au lieu du déployement local, le site web est maintenant déployé en utilisant `Flask` et Render services pour le rendre plus accessible.

