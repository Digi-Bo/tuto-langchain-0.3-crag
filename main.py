# main.py
# Ce fichier sert de point d'interaction avec l'utilisateur via une interface en ligne de commande.
# Il permet à l'utilisateur de poser des questions ou de quitter l'application.
# Les questions sont transmises à une fonction qui gère leur traitement et génère des réponses.
# Le menu principal guide l'utilisateur dans ses choix.

from colorama import Fore  # Bibliothèque utilisée pour styliser la sortie dans le terminal.
from query import query  # Fonction importée depuis query.py pour traiter les questions.

def start():
    """
    Affiche le menu principal de l'application et gère la navigation.
    L'utilisateur peut choisir entre poser une question ou quitter l'application.
    """
    instructions = (
        """How can I help you today?\n"""  # Message affiché pour introduire l'application.
    )
    print(Fore.BLUE + "\n\x1B[3m" + instructions + "\x1B[0m" + Fore.RESET)  # Affiche le message en bleu et en italique.

    # Menu principal avec deux options.
    print("MENU")
    print("====")
    print("[1]- Ask a question")  # Option pour poser une question.
    print("[2]- Exit")  # Option pour quitter l'application.
    choice = input("Enter your choice: ")  # Récupère le choix de l'utilisateur.

    if choice == "1":
        ask()  # Si l'utilisateur choisit "1", il est redirigé vers la fonction `ask`.
    elif choice == "2":
        print("Goodbye!")  # Si l'utilisateur choisit "2", un message d'adieu est affiché.
        exit()  # L'application se ferme.
    else:
        print("Invalid choice")  # Si l'utilisateur entre une valeur non valide, un message d'erreur s'affiche.
        start()  # Retour au menu principal pour permettre une nouvelle tentative.

def ask():
    """
    Permet à l'utilisateur de poser des questions.
    Gère les questions et envoie les réponses obtenues depuis la fonction `query`.
    """
    while True:
        user_input = input("Q: ")  # Récupère la question posée par l'utilisateur.
        if user_input == "x":  # Si l'utilisateur entre "x", il retourne au menu principal.
            start()
        else:
            response = query(user_input)  # Appelle la fonction `query` pour traiter la question et obtenir une réponse.
            print(Fore.BLUE + "\n=== ANSWER ====")  # Affiche un en-tête pour la réponse.
            print("A: " + response + Fore.RESET)  # Affiche la réponse en bleu.
            print(Fore.WHITE + 
                  "\n-------------------------------------------------")  # Ligne de séparation après la réponse.

# Point d'entrée principal du programme.
if __name__ == "__main__":
    start()  # Lance l'application en appelant la fonction `start`.
