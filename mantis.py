from random import sample, choices, uniform
from collections import Counter
from time import sleep


def typedPrint(words, newLine=True):
    for char in words:
        sleep(uniform(0, 0.08))
        print(char, end='', flush=True)
    if newLine:
        print()


def typedInput(words, default=None):
    typedPrint(words, newLine=False)
    return (input() or default)


class Card:
    def __init__(self, colorOptions):
        self.backColors = sample(colorOptions, 3)
        self.frontColor = sample(self.backColors, 1)[0]

    def showBack(self):
        typedPrint("The back colors are: " + ', '.join(self.backColors))

    def showFront(self):
        typedPrint("The front color is: " + self.frontColor)

    def showBothSides(self):
        print("The back colors are: " + ', '.join(self.backColors))
        print("The front color is: " + self.frontColor)


class Player:
    def __init__(self, name, colorOptions):
        self.name = name
        self.tank = Counter(choices(colorOptions, k=4))
        self.scorePile = dict.fromkeys(colorOptions, 0)

    @property
    def scoreTotal(self):
        return sum(self.scorePile.values())

    def greet(self):
        typedPrint("Welcome, " + self.name + "!")

    def show(self):
        print(self.name + ":")
        print(" tank: " + str({k: v for k, v in self.tank.items() if v > 0}))
        print(" scorePile: " +
              str({k: v for k, v in self.scorePile.items() if v > 0}))
        print(" scoreTotal: " + str(self.scoreTotal))

    def score(self, card):
        color = card.frontColor
        if self.tank[color] == 0:
            self.tank[color] += 1
            typedPrint(color + " is not in tank, adding it...")
        else:
            self.scorePile[color] += (self.tank[color] + 1)
            self.tank[color] = 0
            typedPrint(color + " is in tank! Moving cards to score pile...")

    def steal(self, card, opponent):
        color = card.frontColor
        opponentTankColors = [
            k for k, v in opponent.tank.items() if v > 0]
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


if __name__ == "__main__":

    # Define all available color options
    colorOptions = ['Yellow', 'Red', 'Green',
                    'Purple', 'Blue', 'Orange', 'Pink']

    # Configure the game ----------------------------------------
    typedPrint("Lets set up the game!")
    nPlayers = int(typedInput("How many people will be playing? ", 2))
    print()

    players = {}
    for n in range(nPlayers):
        playerName = input("Name for player{n}: ".format(n=n+1))
        players[playerName] = Player(playerName, colorOptions)

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
            typedInput(player.name + ", press Enter to draw a card...")
            typedPrint(player.name + " drew a card...")
            drawnCard = Card(colorOptions)
            drawnCard.showBack()

            # Decide to try and score or steal
            choice = input("Would you like to score or steal? ").upper()
            while choice not in ['SCORE', 'STEAL']:
                choice = input("Would you like to score or steal? ").upper()

            if choice == 'SCORE':
                drawnCard.showFront()
                player.score(drawnCard)

            if choice == 'STEAL':
                opponents = [pn for pn, p in players.items()]
                opponents.remove(player.name)
                opponent = input("From who? ")
                while opponent not in opponents:
                    opponent = input("From who? ")

                drawnCard.showFront()
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
