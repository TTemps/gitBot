from git import Repo
import os
import datetime
from io import BytesIO
import logging
import weather

logging.basicConfig(filename='log_commit.txt', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s', encoding='utf-8')
logging.basicConfig(filename='error_commit.txt', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s', encoding='utf-8')

# Liste des fêtes avec les messages correspondants
holidays = [
    (datetime.date(datetime.date.today().year, 1, 1), " - Bonne année! 🎉"),
    (datetime.date(datetime.date.today().year, 2, 14), " - Bonne Saint-Valentin! 💘"),
    (datetime.date(datetime.date.today().year, 5, 1), " - Joyeuse fête du travail! 🌷"),
    (datetime.date(datetime.date.today().year, 7, 14), " - Bonne fête nationale! 🇫🇷"),
    (datetime.date(datetime.date.today().year, 8, 15), " - Joyeuse fête de l'Assomption! 🌺",),
    (datetime.date(datetime.date.today().year, 11, 1), " - Joyeuse fête de la Toussaint! 🍂",),
    (datetime.date(datetime.date.today().year, 11, 11), " - Bonne fête de l'Armistice! 🕊️",),
    (datetime.date(datetime.date.today().year, 12, 25), " - Joyeux Noël! 🎄"),
]

def create_commit(commit_message, message):
    """
    Créer un commit avec le message spécifié
        commit_message: le message du commit
    """
    try:
        repo = Repo(".")
        index = repo.index
        add_commit_message_to_file("message.txt", commit_message + message) # Ajouter le message au fichier
        index.add(["message.txt"])
        #get the first list of the message.txt
        index.commit(commit_message) # Commit le message
        origin = repo.remote("origin")
        origin.push()
        logging.info("Commit effectué avec succès!\n")
    except Exception as e:
        logging.error(f"Erreur lors du commit : {e}")
        exit(1)

def add_commit_message_to_file(filename, commit_message): # Ajouter le message complet au fichier
    """
    Ajouter le message complet au fichier
        filename: le nom du fichier
        commit_message: le message du commit"""
    with open(filename, "a", encoding='utf-8') as file:
        file.write(f"{commit_message}\n")

def get_days_until_new_year(): # Récupérer le nombre de jours restants jusqu'à la nouvelle année
    """
    Récupérer le nombre de jours restants jusqu'à la nouvelle année
    return: le nombre de jours restants jusqu'à la nouvelle année"""
    today = datetime.date.today()
    new_year = datetime.date(today.year + 1, 1, 1)
    days_left = (new_year - today).days
    return days_left

def get_number_days_year(): # Récupérer le nombre de jours dans l'année courante
    """
    Récupérer le nombre de jours dans l'année courante
    return: le nombre de jours dans l'année courante"""
    today = datetime.date.today()
    first_day = datetime.date(today.year + 1, 1, 1)
    last_day = datetime.date(today.year + 1, 12, 31)
    total_day = (last_day - first_day).days
    return total_day

def initialize_message_file(): # Initialiser le fichier message.txt si nécessaire
    """
    Initialiser le fichier message.txt si nécessaire
    """
    initialized = False 
    if not os.path.exists("message.txt"):
        logging.info("Création du fichier 'message.txt'.")
        with open("message.txt", "w", encoding='utf-8') as file:
            file.write("Initialisation du fichier 'message.txt'.\n")
        initialized = True
    with open("message.txt", "r", encoding='utf-8') as file:
        content = file.read()
        if not content.strip() and not initialized:
            logging.info("Ajout du message initial dans 'message.txt'.")
            with open("message.txt", "w", encoding='utf-8') as file:
                file.write("Initialisation du fichier 'message.txt'.\n")
    if initialized:
        create_commit("Initialisation du fichier 'message.txt'.")
        
def set_message():
    """
    Définir le message du commit
    return: le message du commit"""
    days_left = get_days_until_new_year()
    commit_message = f"Commit {get_number_days_year()-days_left+1}/{get_number_days_year()} : {days_left} jours restants"
    message = ""
    weather_data = weather.get_weather()
    message += f"""\nMétéo : 
        - Température {weather_data['temperature']} 
        - Cycle : {weather_data['is_day']} 
        - Temps :{weather_data['weather_code']}
        - Lever : {weather_data['sunrise']}
        - Coucher : {weather_data['sunset']}\n"""
    return commit_message,message

def get_last_commit_message(): # Récupérer le message du dernier commit
    """
    Récupère le message du dernier commit
    return: le message du dernier commit
    """
    try:
        repo = Repo(".")
        last_commit = list(repo.iter_commits("main", max_count=1))[0]
        last_commit_message = last_commit.message
        return last_commit_message
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du dernier commit : {e}")
        return ""

def is_commit_content_identical(last_commit_message, commit_message): # Vérifier si le contenu du fichier est identique au dernier commit
    """
    Vérifie si le contenu du fichier est identique au dernier commit
    return: True si le contenu est identique, False sinon
    """
    return last_commit_message.strip() == commit_message.strip()

def main():
    """
    Fonction principale
    """
    commit_message, message = set_message()
    # Vérifier si c'est l'une des fêtes spéciales
    for holiday_date, holiday_message in holidays:
        if datetime.date.today() == holiday_date:
            commit_message += holiday_message
    logging.info("Message du commit actuel : " + commit_message)
    last_commit_message = get_last_commit_message()
    logging.info("Message du dernier commit : " + last_commit_message)

    # Vérifier si le contenu du fichier est identique au dernier commit
    if is_commit_content_identical(last_commit_message, commit_message):
        logging.info("Aucun changement détecté, pas de commit effectué.")
    else:
        logging.info("Print avant commit : " + commit_message)
        create_commit(commit_message , message)
    return

if __name__ == "__main__":
    initialize_message_file()  # Initialiser le fichier message.txt si nécessaire
    main()  # Exécute le script principal
