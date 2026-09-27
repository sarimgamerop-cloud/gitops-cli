# Github Package:
from github import Github
from github import Auth
from github.GithubException import UnknownObjectException
import os, subprocess
from colorama import Fore, Style, init
init(autoreset=True)

from dotenv import load_dotenv
load_dotenv()

token = os.environ["GITHUB_TOKEN"]
g = Github(auth=Auth.Token(token))

# Global Variables
user = g.get_user()
username = user.login

def user_dec(x):
    while True:
        print(x,"(y/n) : ",end="")
        status = input().lower().strip()

        if status in ('yes','y'):
            return True
        elif status in ('no','n'):
            return False
        else:
            print("Enter a valid value (y/n).")

def help():
    # helpful help() command.
    print('''----- Available Options -----
help: displays this help,
fetch: fetches all repos,
create_repo: creates a repository,
delete_repo: deletes a repository,
clone_repo: clones a repository,
list_contents: lists the contents of a repository''')

def repo_fetch():
    # fetches all the repositories and list them:
    for repo in g.get_user().get_repos():
        print(Fore.GREEN + f"• {repo.full_name}" + Style.RESET_ALL)

def create_repository(name):
    # Creates a repo and add <repo> as its object:
    repo = user.create_repo(
    name=name,
    private = user_dec("Is the repo private"),
    description=input("Enter description: "),
    auto_init=user_dec("Do want to create a inital commit/README")
    )
    print(f"Created: {repo.full_name}") # Done...

def delete_repository(name):
    try:
        repo = g.get_repo(f"{username}/{name}")

        if user_dec(f"Permanently delete {name}"):
            repo.delete()
            print(f"Permanently deleted: {name}")

    except UnknownObjectException:
        print(f"Repo with the name {name} does not exist.")

def clone_repo(name_repo):
    repo_link = f'https://github.com/{g.get_user().login}/{name_repo}'
    output_directory = str(input('Clone Location: ( blank/default ): '))
    if os.path.exists(output_directory):
        pass
    else:
        print(Fore.RED + 'enter a valid directory!' + Style.RESET_ALL )

    print(Fore.YELLOW + 'Cloning to the Repository ...' + Style.RESET_ALL )

    subprocess.run(['git',
        'clone',
        repo_link,
        output_directory]
    )
    print(Fore.YELLOW + f"Cloned to '{output_directory}'.")

def list_contents(name):
    usrnme = g.get_user().login
    try:
        repo = g.get_repo(f"{usrnme}/{name}")
    except UnknownObjectException:
        print(f"Repo with the name {name} does not exist.")
    else:
        for files in repo.get_contents(""):
            # it wont be that simple...
            print(files.name) # files.name just works....

def create_file(name):
    repo = g.get_repo(f"{username}/{name}")
    repo.create_file(input('Enter file name: '),input("Enter commit message: "),"")

def delete_file(name):
    repo = g.get_repo(f"{username}/{name}")
    file_name = input("Enter file name to delete: ")
    contents = repo.get_contents(file_name)
    if user_dec(f"Delete file '{file_name}' from {repo.full_name}"):
        repo.delete_file(file_name, "", contents.sha)
        print(f"Succesfully deleted '{file_name}'")
def decide(cmd):
    # decide function: handles commands system.

    ## 'fetch': dynamically fetches repositories
    if cmd == 'fetch':
        print(Fore.YELLOW + "Repositories-List:" + Style.RESET_ALL)
        repo_fetch()

    ## 'help': calls the help function
    elif cmd == 'help':
        help()

    elif cmd == 'whoami':
        print("USERNAME:",username)

    ## 'create_repo': creates a repositories with optional arguments.
    elif cmd == 'create_repo':
        repo_name = str(input("Give your repository a name" + Fore.YELLOW + " (str/)" + Style.RESET_ALL + ": "))
        create_repository(repo_name)

    ## 'delete_repo': deletes a repository from account.
    elif cmd == 'delete_repo':
        delete_repository(input("Enter repo name to delete: ").strip())

    ## 'list_contents': lists all the contents of a repository
    elif cmd == 'list_contents':
        list_contents(input("Enter repo name to list contents: ".strip()))

    elif cmd == 'create_file':
        create_file(input("Enter repo name: "))

    elif cmd == 'delete_file':
        delete_file(input("Enter repo name: "))

    ## 'clone_repo': clones a repository in local storage
    elif cmd == 'clone_repo':
        clone_repo(input('Enter Repository name: '))

    else:
        print('command:'+ Fore.RED + ' null' + Style.RESET_ALL)

while True: # Fun Fact: it's always true
    commands = str(input(Fore.GREEN + "~> " + Style.RESET_ALL)).strip()
    decide(commands)
