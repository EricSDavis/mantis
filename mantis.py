import random
from random import sample, choices, uniform
from collections import Counter
from time import sleep
from typing import Literal

# Functions for mimicking human typing
def typedPrint(words: str, newLine=True) -> None:
    for char in words:
        sleep(uniform(0, 0.08))
        print(char, end='', flush=True)
    if newLine:
        print()


def typedInput(words: str, default=None) -> str:
    typedPrint(words, newLine=False)
    return (input() or default)


# Functions for colorizing strings, lists, and dictionaries
def color(text: str, color: Literal["Yellow", "Red", "Green", "Purple", "Blue", "Orange", "Pink"]) -> str:
    END = '\033[1;37;0m'
    if color == "Yellow":
        return str('\033[1;93;48m' + text + END)
    if color == "Red":
        return str('\033[1;31;48m' + text + END)
    if color == "Green":
        return str('\033[1;32;48m' + text + END)
    if color == "Purple":
        return str('\033[38;5;93m' + text + END)
    if color == "Blue":
        return str('\033[1;34;48m' + text + END)
    if color == "Orange":
        return str('\033[38;5;208m' + text + END)
    if color == "Pink":
        return str('\033[38;5;219m' + text + END)


def colorDict(d: dict) -> str:
    return ", ".join([color(k + ": " + str(v), k) for k, v in d.items() if v > 0])


def colorList(l: list[str]) -> str:
    return ", ".join([color(v, v) for v in l])


class Card:
    def __init__(self, colorOptions: list[str]) -> None:
        self.backColors = sample(colorOptions, 3)
        self.frontColor = sample(self.backColors, 1)[0]

    def showBack(self) -> None:
        typedPrint("The back colors are: " + colorList(self.backColors))

    def showFront(self) -> None:
        front = self.frontColor
        typedPrint("The front color is: " + color(front, front))

    def showBothSides(self) -> None:
        print("The back colors are: " + ', '.join(self.backColors))
        print("The front color is: " + self.frontColor)


class Player:
    def __init__(self, name, colorOptions):
        self.name = name
        self.tank = Counter(choices(colorOptions, k=4))
        self.scorePile = dict.fromkeys(colorOptions, 0)

    @property
    def scoreTotal(self) -> int:
        return sum(self.scorePile.values())

    def greet(self) -> None:
        typedPrint("Welcome, " + self.name + "!")

    def show(self) -> None:
        print(self.name + ":")
        print(" tank: " + colorDict(self.tank))
        print(" scorePile: " + colorDict(self.scorePile))
        print(" scoreTotal: " + str(self.scoreTotal))

    def tankColors(self) -> list[str]:
        return [k for k, v in self.tank.items() if v > 0]

    def score(self, card: Card) -> None:
        color = card.frontColor
        if self.tank[color] == 0:
            self.tank[color] += 1
            typedPrint(color + " is not in tank, adding it...")
        else:
            self.scorePile[color] += (self.tank[color] + 1)
            self.tank[color] = 0
            typedPrint(color + " is in tank! Moving cards to score pile...")

    def steal(self, card: Card, opponent: "Player") -> None:
        color = card.frontColor
        opponentTankColors = opponent.tankColors()
        if color in opponentTankColors:
            self.tank[color] += (opponent.tank[color] + 1)
            opponent.tank[color] = 0
            typedPrint(("{o} has {c} in their tank. "
                        "Steal successful :) moving to {s}'s tank...")
                       .format(o=opponent.name, c=color, s=self.name))
        else:
            opponent.tank[color] = 1
            typedPrint(("{o} doesn't have {c} in their tank. "
                        "Steal failed :( moving to {o}'s tank...")
                       .format(o=opponent.name, c=color, s=self.name))
            
class NPC(Player):
    def __init__(self, name, colorOptions):
        super().__init__(name, colorOptions)

    def scoreOrSteal(self, card: Card, opponents=dict[Player]) -> Literal['SCORE', 'STEAL']:
        card_colors = set(card.backColors)
        my_tank_colors = set(self.tankColors())
        max_score_count = len(card_colors.intersection(my_tank_colors))
        
        steal_counts = []
        for on, o in opponents.items():
            opp_tank_colors = set(o.tankColors())
            steal_counts.append(len(card_colors.intersection(opp_tank_colors)))
        max_steal_count = max(steal_counts)
        
        return 'SCORE' if max_score_count >= max_steal_count else 'STEAL'
    
    def chooseOpponent(self, card: Card, opponents: dict[Player]) -> str:
        card_colors = set(card.backColors)
        steal_counts = {}
        for on, o in opponents.items():
            opp_tank_colors = set(o.tankColors())
            steal_counts[on] = len(card_colors.intersection(opp_tank_colors))
        return random.choice([k for k, v in steal_counts.items() if v == max(steal_counts.values())])


if __name__ == "__main__":

    # Define all available color options
    colorOptions = ['Yellow', 'Red', 'Green',
                    'Purple', 'Blue', 'Orange', 'Pink']

    # Configure the game ----------------------------------------
    typedPrint("Lets set up the game!")
    nPlayers = int(typedInput("How many real people will be playing? ", 2))
    nNpcs = int(typedInput("How many NPCs will be playing? ", 2))
    while nPlayers < 1:
        typedPrint("There must be at least 1 real player.")
        nPlayers = int(typedInput("How many real people will be playing? ", 2))
    if nPlayers < 2 and nNpcs < 1:
        typedPrint("You need at least one NPC to play by yourself.\n")
        typedPrint("Adding an NPC")
        nNpcs = 1
    print()

    real_players = {}
    for n in range(nPlayers):
        playerName = input(f"Name for player{n+1}: ")
        real_players[playerName] = Player(playerName, colorOptions)

    npcs = {}
    for n in range(nNpcs):
        npcName = input(f"Name for NPC{n+1} (default: NPC{n+1}): ") or f"NPC{n+1}"
        npcs[npcName] = NPC(npcName, colorOptions)
    
    players = {**real_players, **npcs}

    print()
    for playerName, player in players.items():
        player.greet() 

    print()
    winningScore = int(
        typedInput("Set the number of points required to win (we suggest 10): ", 10))

    # Begin gameplay ---------------------------------------------
    typedPrint("Let's deal the first hand...")
    round = 1
    currentLeadingPlayer = ""
    currentLeadingScore = 0
    while currentLeadingScore < winningScore:

        # Define a round of gameplay
        for playerName, player in players.items():

            print("\nCurrent Standings (Round {round}):".format(round=round))
            for pn, p in players.items():
                p.show()
                print()
            print()
            sleep(0.2)

            # Draw a random card
            if type(player) == Player:    
                typedInput(player.name + ", press Enter to draw a card...")
            typedPrint(player.name + " drew a card...")
            drawnCard = Card(colorOptions)
            drawnCard.showBack()

            # List opponents
            opponents = {pn: p for pn, p in players.items() if pn != playerName}
            opponentNames = [pn for pn, p in opponents.items()]

            # Decide to try and score or steal (NPC)
            if type(player) == NPC:
                choice = player.scoreOrSteal(card=drawnCard, opponents=opponents)

                ## Choose opponent
                if choice == 'STEAL':
                    opponent = player.chooseOpponent(card=drawnCard, opponents=opponents)
                    typedPrint(f"{player.name} chose to {choice.lower()} from {opponent}")
                
                else:
                    typedPrint(f"{player.name} chose to {choice.lower()}")

            # Decide to try and score or steal (Player)
            if type(player) == Player:  
                choice = input("Would you like to score or steal? ").upper()
                while choice not in ['SCORE', 'STEAL']:
                    choice = input("Would you like to score or steal? ").upper()       

                ## Choose opponent
                if choice == 'STEAL':
                    if len(opponents) == 1:
                        opponent = opponentNames[0]
                    else:
                        opponent = input("From who? ")
                        while opponent not in opponents:
                            opponent = input("From who? ")     
            
            # Show card
            drawnCard.showFront()

            # Perform score or steal
            match choice:
                case 'SCORE':
                    player.score(drawnCard)
                case 'STEAL':
                    player.steal(drawnCard, players[opponent])

            sleep(0.2)

            # Check for a winner
            if player.scoreTotal > currentLeadingScore:
                currentLeadingPlayer = player.name
                currentLeadingScore = player.scoreTotal
            if currentLeadingScore >= winningScore:
                break

        # Increment the round
        round += 1

    print("Congratulations, " + currentLeadingPlayer + ", you win!")
