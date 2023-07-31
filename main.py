from git import Repo
import os
import datetime

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
    repo = Repo(".")
    index = repo.index
    # Inclure tous les fichiers modifiés dans l'index
    add_commit_message_to_file("message.txt", commit_message)
    index.add(["message.txt"])

    # Effectuer le commit avec le message de commit et les fichiers modifiés
    index.commit(commit_message)

    # Vérifier si le contenu du fichier est identique au dernier commit
    if repo.is_dirty():
        origin = repo.remote("origin")
        origin.push()
        print("Commit effectué avec succès!")
    else:
        print(
            "AsAucune modification depuis le dernier commit. Le commit n'a pas été effectué."
        )


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


def initialize_message_file():
    if not os.path.exists("message.txt"):
        print("Initialisation du fichier 'message.txt'.")
        with open("message.txt", "w") as file:
            file.write("Initialisation du fichier 'message.txt'.")
        create_commit("Initialisation du fichier 'message.txt'.")


def is_file_content_identical(file_path, content):
    if not os.path.exists(".git"):
        return False

    repo = Repo(".")
    last_commit = repo.head.commit

    for item in last_commit.tree.traverse():
        if item.path == file_path:
            last_commit_blob = item
            last_commit_content = last_commit_blob.data_stream.read().decode("utf-8")
            print(
                "contenu actuel : " + content.strip(),
                "\ncontenu du last : " + last_commit_content.strip(),
            )
            return content.strip() == last_commit_content.strip()

    return False


def main():
    days_left = get_days_until_new_year()
    commit_message = f"Commit {get_number_days_year()-days_left+1}/{get_number_days_year()} : {days_left} days left"

    # Vérifier si c'est l'une des fêtes spéciales
    for holiday_date, holiday_message in holidays:
        if datetime.date.today() == holiday_date:
            commit_message += holiday_message
    # Vérifier si le contenu du fichier est identique au dernier commit
    if is_file_content_identical("message.txt", commit_message):
        print(
            "Aucune modification depuis le dernier commit. Le commit n'a pas été effectué."
        )
    else:
        print("Print avant commit : " + commit_message)
        create_commit(commit_message)
    return


if __name__ == "__main__":
    main()
