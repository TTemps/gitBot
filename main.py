from git import Repo
import os
import datetime


def create_commit(commit_message):
    repo = Repo(".")
    index = repo.index
    # Inclure tous les fichiers modifiés dans l'index
    index.add(["message.txt"])

    # Effectuer le commit avec le message de commit et les fichiers modifiés
    index.commit(commit_message)

    origin = repo.remote(name="origin")
    origin.push()


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


def main():
    days_left = get_days_until_new_year()
    commit_message = f"Commit {get_number_days_year()-days_left+1}/{get_number_days_year()} : {days_left} days left"
    print(commit_message)
    create_commit(commit_message)


if __name__ == "__main__":
    main()

