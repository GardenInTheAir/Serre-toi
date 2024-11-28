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

## Points en travaille encore
La connexion à la base de données est encore problèmatique après le déployement sur le cloud de Render dû au timeout des requêtes. Pour le moment, je suggère l'installation de l'application et la parcourire localement pour accéder à l'application au complet et essayer tous ces fonctionnements (par exemple la création d'un compte ou la resérvation d'activités). La réparation de l'accès à la BD lors du déployement sur le cloud est en cours. Merci de patienter un peu avant de pouvoir utiliser l'application web au complet en suivant le lien de déployement en ligne.

## Étapes d'installation et de parcours local de l'application

### Prérequis
Assurez-vous d'avoir le éléments suivants installés:
- Python 3.13.0 [https://www.python.org/downloads/]
- pip [https://pip.pypa.io/en/stable/installation/]
- Git [https://git-scm.com/]

### Installations
Ces installations sont pour Windows. Les étapes d'iinstallations pour Linux ne sont pas fournis. Les étapes doivent être presque les mêmes juste avec le changement de comment les lignes de commandes s'écrivent dû à la différence de syntax. Des ressources en lignes peuvent traduire les lignes de commandes ci-dessous en lignes de commande Linux.

1. Clonez le projet depuis ce dépôt GitHub. Vous pouvez copier le lien URL du dépôt et exécuter la commande `git clone <URL_du_depot>`. Puis, changez de repértoire pour aller dans le dossier du dépôt installé en executant `cd <nom_dossier_clone>`.
2. Créez un environnement virtuel pour isoler les dépendances du projet. Executez la commande `python -m venv venv`. Maintenant créé, vous pouvez l'activer avec la commande `venv\Scripts\activate`.
3. Installez les dépendances en vous plaçant à l'intérieur du dossier du projet avec la commande `pip install -r requirements.txt`.
4. Lancez l'application Flask pour démarrer l'application en exécutant `python index.py`.

Par défaut, l'application sera accessible à l'adresse `http://127.0.0.1:5000`.

### Gestion d'erreurs
- Si vous rencontrez un problème de port déjà utilisé pour le port par défaut `5000`, vous pouvez spécifier un autre port en exécutant `python index.py --port=5001`.
- Si vous rencontrez un problème de connexion à la base de données pour démarrer l'application, c'est probablement que la base de données est entrée en hibernation. Dans ce cas, vous pouvez créer un issue sur ce dépôt GitHub pour que je puisse fixer le problème.

#### Comment créer un issue ?
Vous pouvez signaler un issue pour tout genre de problème, non seulement un problème de connection à la base de données, si jamais vous rencontrez de erreurs lors du démarrage ou du parcours de l'application et vous avez besoin de l'assistance pour vous débloquer. 
1. Allez sur la page du dépôt GitHub ici.
2. Cliquez sur l'onglet `Issues`.
3. Sélectionnez `New Issue`.
4. Décrivez le problème rencontré avec le plus de détails possibles comme :
   - Les étapes que vous avez fait pour arriver à ce problème.
   - Les messages d'erreurs obtenus.
   - Toute autre information utile (par exemple la version de dépendances).

