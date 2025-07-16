import random
from ascii_art import *


class Kniffel:
    CATEGORIES ={
        '1': 'Einer',
        '2': 'Zweier',
        '3': 'Dreier',
        '4': 'Viere',
        '5': 'Fünfer',
        '6': 'Sechser',
        '7': 'Dreierpasch',
        '8':'Viererpasch',
        '9': 'Fullhause',
        '10': 'Kleine Straße',
        '11':'Große Straße',
        '12': 'Kniffel/Yahtzee',
        '13':'Chance',

    }
    obere_Bonus=35
    obere_min_punkte=63

    def __init__(self, Players):

        self.players = Players
        self.Scores = {Player:{cat: None for cat in self.CATEGORIES.keys() }for Player in Players}
        self.current_players_index=0
        self.round=1
        self.rounds=(len(self.CATEGORIES))
        self.game_over=False


    def current_Player(self):
        return self.players[self.current_players_index] # aktuelle Spieler

    def roll_wurfeln(self,num_wurfeln=5):
        return [random.randint(1,6) for w in range(num_wurfeln)] #

    def akteull_category(self, wurfeln, category):
        wurfeln = sorted(wurfeln)
        counts = [wurfeln.count(i) for i in range(1, 7)]

        if category == "1":
            return counts[0]*1
        elif category =="2":
            return  counts[1]*2
        elif category =="3":
            return counts[2]*3
        elif category =="4":
            return counts[3]*4
        elif category== "5":
            return counts[4]*5
        elif category=="6":
            return counts[5]*6
        elif category=="7":
            return sum(wurfeln) if max(counts) >=3 else 0
        elif category=="8":
            return sum(wurfeln) if max(counts) >=4 else 0
        elif category=="9":
            return 25 if (2 in counts and 3 in counts) else 0
        elif category=="10":
            straights = [set([1, 2, 3, 4]), set([2, 3, 4, 5]), set([3, 4, 5, 6])]
            wurfel_set = set(wurfeln)
            return 30 if any(st.issubset(wurfel_set) for st in straights) else 0
        elif category=="11":
            return 40 if wurfeln in [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]] else 0
        elif category=="12":
            return 50 if len(set(wurfeln)) == 1 else 0
        elif category=="13":
            return sum(wurfeln)
        return 0

    def kalkulation_total_scores(self , player):

        score_karte=self.Scores[player]
        oberer_sum= sum(
            score_karte[cat] or 0
            for cat in ['1','2','3','4','5','6']

        )
        bonus= self.obere_Bonus if oberer_sum >= self.obere_min_punkte else 0
        untere_sum= sum(
            score_karte[cat] or 0
            for cat in ['7','8','9','10',
                        '11','12','13']


        )
        return oberer_sum+ bonus +untere_sum

    def zeige_scorecard(self, player):
        score_karte = self.Scores[player]
        print(f"\nPunktetabelle für {player}: ")
        print("-*-"*10)

        # Obere Sektion
        obere_sum=0
        print("\nObere Sektion:")
        for cat in ['1','2','3','4','5','6']:
            punkte = score_karte[cat] if score_karte[cat] is not None else 0
            obere_sum += punkte
            print(f"{self.CATEGORIES[cat]:<15}: {punkte}")

        bonus = self.obere_Bonus if obere_sum >= self.obere_min_punkte else 0
        print(f"{'Bonus (ab 63 Punkte)':<18}: {bonus}")
        print("-*-"*10)

        # Untere Sektion

        untere_sum=0
        print("\nUntere Sektion:")
        for cat in ['7','8','9','10','11','12','13']:
            punkte= score_karte[cat] if score_karte[cat] is not None else 0
            untere_sum += punkte
            print(f"{self.CATEGORIES[cat]:<18}: {punkte}")

        print("-"*30)
        tolal= obere_sum+ bonus+untere_sum
        print(f"Gesamtpunkte: {tolal}")
        print("-*-"*10)

    def aktuelle_categories(self, player):
        return  [cat for cat, score in self.Scores[player].items() if score is None]


    def next_player(self):
        self.current_players_index = (self.current_players_index + 1) % len(self.players)
        if self.current_players_index==0:
            self.round +=1
            if self.round > self.rounds:
                self.game_over= True

    def play_reihe(self):
        player = self.current_Player()
        print(f"\n {player} ist an der Reihe (Runde  {self.round})")

        wurflen = self.roll_wurfeln()
        behalten_wurfeln_haupt = []
        behalten_wurfeln1=[]
        behalten_wurfeln2=[]
        behalten_wurfeln3=[]
        num_neu_wurfel = 5
        runden = 1




        # Würfel behalten
        while runden < 3:

            if runden == 1:

                print(f"\nWurf {runden}: {wurflen}")
                print("Um dein Zug zu überspringen drück auf 'q'")
                behalten_Eingabe = input("Welche Würfel behatlen? (index 0-4, komma-getrennt, leer taste = alle neu): ")
                if behalten_Eingabe.lower() == "q":
                    break





                if behalten_Eingabe:
                    behalten_index = [int(i.strip()) for i in behalten_Eingabe.split(',') if i.strip().isdigit()]
                    behalten_wurfeln1 = [wurflen[i] for i in behalten_index if 0 <= i < len(wurflen)]

                    # neue würfel werfen

                    num_neu_wurfel = 5 - len(behalten_wurfeln1)
                    print("Behaltene Würfel:", behalten_wurfeln1)

                wurflen = self.roll_wurfeln(num_neu_wurfel)
                runden += 1

            if runden == 2:
                print(f"\nWurf {runden}: {wurflen}")
                print("Um dein Zug zu überspringen drück auf 'q'")
                behalten_Eingabe = input("Welche Würfel behatlen? (index 0-4, komma-getrennt, leer taste = alle neu): ")
                if behalten_Eingabe.lower() == "q":
                    break


                if behalten_Eingabe:
                    behalten_index = [int(i.strip()) for i in behalten_Eingabe.split(',') if i.strip().isdigit()]
                    behalten_wurfeln2 = [wurflen[i] for i in behalten_index if 0 <= i < len(wurflen)]
                    behalten_wurfeln_haupt = (behalten_wurfeln1 + behalten_wurfeln2)
                    # neue würfel werfen

                    num_neu_wurfel = num_neu_wurfel - len(behalten_wurfeln2)
                    print("Behaltene Würfel:", behalten_wurfeln_haupt)

                wurflen = self.roll_wurfeln(num_neu_wurfel)
                runden += 1

            if runden == 3:
                print(f"\nWurf {runden}: {wurflen}")
                print("Um dein Zug zu überspringen drück auf 'q'")
                behalten_Eingabe = input("Welche Würfel behatlen? (index 0-4, komma-getrennt, leer taste = alle neu): ")

                if behalten_Eingabe.lower() == "q":
                    break


                if behalten_Eingabe:
                    behalten_index = [int(i.strip()) for i in behalten_Eingabe.split(',') if i.strip().isdigit()]
                    behalten_wurfeln3 = [wurflen[i] for i in behalten_index if 0 <= i < len(wurflen)]
                    behalten_wurfeln_haupt = (behalten_wurfeln_haupt + behalten_wurfeln3)
                    # neue würfel werfen

                    num_neu_wurfel = num_neu_wurfel - len(behalten_wurfeln3)
                    print("Behaltene Würfel:", behalten_wurfeln_haupt)

                wurflen = self.roll_wurfeln(num_neu_wurfel)
                runden += 1
            print(f"\nEndgültige Würfel: {behalten_wurfeln_haupt+wurflen}")

        # Kategorie auswählen
        vorhandne_kate = self.aktuelle_categories(player)
        while True:
            print("\nVerfügbare Kategorien: ")
            for i, cat in enumerate(vorhandne_kate, 1):
                punkten = self.akteull_category(wurflen+behalten_wurfeln_haupt, cat)
                print(f"{i}. {self.CATEGORIES[cat]} (Punkte: {punkten})")

            cat_auswahl = input("Kategorie wählen (1-{}): ".format(len(vorhandne_kate)))
            if cat_auswahl.lower() == "q":
                return False
            if cat_auswahl.isdigit():
                auswahl_index = int(cat_auswahl) - 1
                if 0 <= auswahl_index < len(vorhandne_kate):
                    ausgenomen_kat = vorhandne_kate[auswahl_index]
                    punkten = self.akteull_category(wurflen+behalten_wurfeln_haupt, ausgenomen_kat)
                    self.Scores[player][ausgenomen_kat] = punkten
                    print(f"{self.CATEGORIES[ausgenomen_kat]} mit {punkten} Punkten eingetragen!")
                    break
        self.zeige_scorecard(player)
        self.next_player()
        return True

    def final_ergibnis(self):
        print("\n"+"-*-"*10)
        print(SPIELENDE_ERGEBNISSE)
        print("-*-"*10)

        player_scores=[]
        for player in self.players:
            total= self.kalkulation_total_scores(player)
            player_scores.append((player, total))
            print(f"{player}: {total} Punkte")

        player_scores.sort(key=lambda  x: x[1], reverse=True)

        print("\n"+Plantzierungen)
        for i, (player, score) in enumerate(player_scores, 1):
            print(f"{i}. Platz: {player} ({score} Punkte)")


        print("\nHerzlich Glückwunsch an den Gewinner: ", player_scores[0][0])


