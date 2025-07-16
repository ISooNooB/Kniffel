import sys
from users import register_user, login_user
#from Kniffel_engine import KniffelGame
from  Funktions import *
import sqlite3
from game_engine import Kniffel
from ascii_art import *



#Hauptmenü
def main_menu():
    current_user = None
    while True:

        print("*" * 30)
        print("*" * 10 + "Dev by ISN" + "*" * 10)
        print("***** Kinffel - HAUPTMENÜ*****")
        print("*" * 30)
        print(Regestrieren)
        print(Anmelden)
        print(beenden)

        choice = input("Auswahl: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            current_user = login_user()
            if current_user:
                game_menu(current_user)
        elif choice == '3':
            print("Auf Wiedersehen!")
            sys.exit()
        else:
            print("Ungültige Eingabe!")




#Sipelmenü
def game_menu(username):
    players = []
    num_players = 0

    while True:
        print("*" * 30)
        print("*" * 10 + "Dev by ISN" + "*" * 10)
        print("***********SPIELMENÜ**********")
        print("-" * 30)
        print(f"Angemeldet als: {username}")
        print(Spieleranzahl_festlegen)
        print(Spieler_hinzufugen)
        print(Spiel_starten)
        print(Abmelden)


        choice = input("Auswahl: ")

        if choice == '1':
            num_players_input = input("Anzahl der Spieler (2-4): ")
            if num_players_input.isdigit() and 2 <= int(num_players_input) <= 4:
                num_players = int(num_players_input)
                players = []
                print(f"Es können {num_players} Spieler hinzugefügt werden.")
            else:
                print("Ungültige Anzahl! (2-4 Spieler)")

        elif choice == '2':
            if num_players == 0:
                print("Bitte zuerst Spieleranzahl festlegen!")
                continue

            if len(players) >= int(num_players):
                print("Maximale Spielerzahl erreicht!")
                continue

            player_name = input("Spielername: ")
            conn = sqlite3.connect('kniffel.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (player_name,))
            if cursor.fetchone():
                players.append(player_name)
                print(f"Spieler {player_name} hinzugefügt!")
            else:
                print("Benutzer existiert nicht!")
            conn.close()

        elif choice == '3':
            if len(players) < 2:
                print("Mindestens 2 Spieler benötigt!")
                continue

            game = Kniffel(players)
            print("\nSpiel startet!")

            while not game.game_over:
                if not game.play_reihe():
                    if confirm_quit():
                        print("Spiel abgebrochen!")
                        return

            game.final_ergibnis()
            return

        elif choice == '4':
            print("Abgemeldet!")
            return
