# README.ME - Application de Calendrier Python

## Description
Cette application Python est conçue pour afficher un calendrier mensuel et permettre aux utilisateurs d'ajouter des tâches pour des jours spécifiques. L'API utilise Flask et SQLite pour stocker les tâches et fournit une API pour récupérer et ajouter des tâches. L'application est réalisée en utilisant la bibliothèque tkinter pour créer une interface utilisateur graphique.

## Fonctionnalités
L'application comporte les fonctionnalités suivantes :

1. **Affichage du Calendrier**
   - L'utilisateur peut entrer un mois (1-12) et une année pour afficher le calendrier du mois correspondant.
   - Le calendrier affiche les jours du mois avec les noms des jours en français.

2. **Ajout de Tâches**
   - L'utilisateur peut sélectionner un jour dans le calendrier affiché.
   - Il peut ensuite ajouter une tâche pour ce jour en saisissant une description de la tâche et en appuyant sur le bouton "Ajouter Tâche".
   - Les tâches ajoutées sont stockées dans la base de données SQLite associées à la date du jour sélectionné.

3. **Affichage des Tâches**
   - L'utilisateur peut sélectionner un jour dans le calendrier pour afficher les tâches associées à ce jour.

## Installation
1. Assurez-vous d'avoir Python 3 installé sur votre système.
2. Installez les bibliothèques Python requises en exécutant la commande suivante :

   ```shell
   pip install flask requests
   ```

## Utilisation
1. Exécutez l'api en exécutant le code Python calandar_api.py :

   ```shell
   python flask_server.py
   ```

   Le serveur sera accessible à l'adresse http://localhost:5000.

2. Exécutez l'application en exécutant le code Python app.py :

   ```shell
   python calendar_app.py
   ```

3. Utilisez l'interface utilisateur pour afficher le calendrier, sélectionner un jour et ajouter des tâches.

## Avertissements
- Assurez-vous que le serveur Flask est en cours d'exécution avant de lancer l'application.
- Le code n'inclut pas de gestion avancée des erreurs ni de gestion de la sécurité, car il est destiné à des fins éducatives.
- L'application pour l'ajout et la visualisation des tâches n'est pas encore fonctionnel.
## Auteur
Ce code a été écrit par BOSGIRAUD Léo.

