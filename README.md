# Git Commit Automatique

Ce script Python vous permet de créer automatiquement des commits Git quotidiens avec des messages spécifiques en fonction du jour de l'année et d'autres critères. Il peut également ajouter des messages pour des jours spéciaux comme les fêtes.

## Fonctionnalités

- Crée des commits automatiques avec des messages spécifiques pour chaque jour de l'année.
- Ajoute des messages pour des jours spéciaux tels que les fêtes.
- Vérifie si le contenu du dernier commit est identique au nouveau message et évite de créer un commit inutile.
- Initialise automatiquement le fichier 'message.txt' si nécessaire.

## Utilisation

1. Assurez-vous d'avoir Git installé sur votre système.
2. Téléchargez le script `main.py` dans votre projet.
3. Exécutez le script en utilisant la commande `python3 main.py`.

Le script initialise automatiquement le fichier 'message.txt' si nécessaire, puis crée un commit avec le message approprié pour la journée en cours. Si le contenu du dernier commit est identique au nouveau message, aucun commit ne sera créé.

## Configuration

- Modifiez la liste des jours fériés dans le script en ajoutant ou supprimant des entrées dans la liste `holidays`.
- Vous pouvez personnaliser davantage le script en ajoutant d'autres conditions ou actions selon vos besoins.

## Auteur

[Auteur du Projet]

## Licence

Ce projet est sous licence [MIT License](LICENSE).
