# GitBot - Commit quotidien jusqu'à la nouvelle année

GitBot est un script Python qui effectue des commits Git automatiques tous les jours, en comptant le nombre de jours restant avant la nouvelle année. Chaque commit contient un message indiquant le nombre de jours restant avant la nouvelle année.

## Fonctionnement du script

Le script `gitBot.py` utilise la bibliothèque GitPython pour interagir avec le dépôt Git local. Il effectue les actions suivantes :

1. Calcule le nombre de jours restant jusqu'à la nouvelle année.
2. Crée un message de commit avec le nombre de jours restant.
3. Ajoute les fichiers modifiés dans l'index pour le commit.
4. Effectue un commit avec le message généré.
5. Pousse les commits vers le dépôt distant spécifié.

## Configuration requise

Assurez-vous d'avoir les éléments suivants avant d'exécuter le script :

1. Python 3.x installé sur votre système.
2. Un dépôt Git local configuré avec votre nom d'utilisateur et votre adresse e-mail.
3. Un dépôt Git distant (par exemple, sur GitHub) configuré comme origine (remote) pour le dépôt local.

## Installation

1. Clonez le dépôt GitBot sur votre système :

   ```bash
   git clone https://github.com/TTemps/gitBot.git
