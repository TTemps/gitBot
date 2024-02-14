from git import Repo
import os
import datetime
from io import BytesIO
import logging
import weather

logging.basicConfig(filename='log_commit.txt', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')
# Liste des fêtes avec les messages correspondants
holidays = [
    (datetime.date(datetime.date.today().year, 1, 1), " - Bonne année! 🎉"),
    (datetime.date(datetime.date.today().year, 5, 1), " - Joyeuse fête du travail! 🌷"),
    (datetime.date(datetime.date.today().year, 7, 14), " - Bonne fête nationale! 🇫🇷"),
    (
        datetime.date(datetime.date.today().year, 8, 15),
        " - Joyeuse fête de l'Assomption! 🌺",
    ),
    (
        datetime.date(datetime.date.today().year, 11, 1),
        " - Joyeuse fête de la Toussaint! 🍂",
    ),
    (
        datetime.date(datetime.date.today().year, 11, 11),
        " - Bonne fête de l'Armistice! 🕊️",
    ),
    (datetime.date(datetime.date.today().year, 12, 25), " - Joyeux Noël! 🎄"),
]


def create_commit(commit_message):
    try:
        repo = Repo(".")
        index = repo.index
        add_commit_message_to_file("message.txt", commit_message)
        index.add(["message.txt"])
        index.commit(commit_message)
        origin = repo.remote("origin")
        origin.push()
        logging.info("Commit effectué avec succès!\n")
    except Exception as e:
        logging.error(f"Erreur lors du commit : {e}")


def add_commit_message_to_file(filename, commit_message):
    with open(filename, "a") as file:
        file.write(f"{commit_message}\n")


def get_days_until_new_year():
    today = datetime.date.today()
    new_year = datetime.date(today.year + 1, 1, 1)
    days_left = (new_year - today).days
    return days_left


def get_number_days_year():
    today = datetime.date.today()
    first_day = datetime.date(today.year + 1, 1, 1)
    last_day = datetime.date(today.year + 1, 12, 31)
    total_day = (last_day - first_day).days
    return total_day


def get_last_line_files(file_path):
    with open(file_path, "rb") as f:
        try:  # catch OSError in case of a one line file
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
    return last_line

def get_last_commit_content(file_path, num_lines=8):
    """
    Récupère le contenu des dernières lignes d'un fichier correspondant à un commit.
    
    Args:
        file_path (str): Chemin du fichier à lire.
        num_lines (int): Nombre de lignes à lire depuis la fin du fichier.
        
    Returns:
        str: Le contenu des dernières lignes du fichier.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # Lire toutes les lignes du fichier et récupérer les dernières 'num_lines' lignes
            lines = file.readlines()[-num_lines:]
            return ''.join(lines).strip()  # Concaténer et nettoyer les lignes
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
        return None

def is_file_content_identical(file_path, content, num_lines=8):
    if not os.path.exists(".git"):
        return False
    
    repo = Repo(".")
    last_commit_content = get_last_commit_content(file_path, num_lines)
    print(last_commit_content)
    print(content)
    # Comparer le contenu prévu pour le commit avec le dernier contenu commité
    return content.strip() == last_commit_content.strip()


def initialize_message_file():
    initialized = False
    if not os.path.exists("message.txt"):
        logging.info("Initialisation du fichier 'message.txt'.")
        with open("message.txt", "w") as file:
            file.write("Initialisation du fichier 'message.txt'.\n")
        initialized = True
    with open("message.txt", "r") as file:
        content = file.read()
        if not content.strip() and not initialized:
            logging.info("Ajout du message initial dans 'message.txt'.")
            with open("message.txt", "w") as file:
                file.write("Initialisation du fichier 'message.txt'.\n")
    if initialized:
        create_commit("Initialisation du fichier 'message.txt'.")
        
# def is_file_content_identical(file_path, content):
#     if not os.path.exists(".git"):
#         return False

#     repo = Repo(".")
#     last_commit = repo.head.commit
#     last_line_message_txt = get_last_line_files(file_path)
#     return content.strip() == last_line_message_txt.strip()

def set_message():
    days_left = get_days_until_new_year()
    message = f"Commit {get_number_days_year()-days_left+1}/{get_number_days_year()} : {days_left} jours restants"
    weather_data = weather.get_weather()
    message += f"""\nMétéo : 
        - Température {weather_data['temperature']} 
        - Cycle : {weather_data['is_day']} 
        - Temps :{weather_data['weather_code']}
        - Lever : {weather_data['sunrise']}
        - Coucher : {weather_data['sunset']}\n"""
    return message
 
def main():
    
    commit_message = set_message()

    # Vérifier si c'est l'une des fêtes spéciales
    for holiday_date, holiday_message in holidays:
        if datetime.date.today() == holiday_date:
            commit_message += holiday_message
            
    logging.info("Contenu actuel : " + commit_message)
    #last_line_message_txt = get_last_line_files("message.txt")
    last_line_message_txt = get_last_commit_content("message.txt")
    logging.info("Contenu du dernier commit : " + last_line_message_txt)
    # Vérifier si le contenu du fichier est identique au dernier commit
    if is_file_content_identical("message.txt", commit_message):
        logging.info("Aucun changement détecté, pas de commit effectué.")
    else:
        logging.info("Print avant commit : " + commit_message)
        create_commit(commit_message)

    return


if __name__ == "__main__":
    initialize_message_file()  # Initialiser le fichier message.txt si nécessaire
    main()  # Exécuter le script principal
