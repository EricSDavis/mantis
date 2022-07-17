import random


class Card:
    def __init__(self, colorOptions):
        self.backColors = random.sample(colorOptions, 3)
        self.frontColor = random.sample(self.backColors, 1)[0]

    def showBack(self):
        print(self.backColors)

    def showFront(self):
        print(self.frontColor)

    def showBothSides(self):
        print("The back colors are: " + ', '.join(self.backColors))
        print("The front color is: " + self.frontColor)


class Player:
    def __init__(self, name, colorOptions):
        self.name = name
        self.tank = dict.fromkeys(colorOptions, 0)
        self.scorePile = dict.fromkeys(colorOptions, 0)

    @property
    def scoreTotal(self):
        return sum(self.scorePile.values())

    def greet(self):
        print("Welcome, " + self.name + "!")

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
            print(color + " is not in tank, adding it...")
        else:
            self.scorePile[color] += (self.tank[color] + 1)
            self.tank[color] = 0
            print(color + " is in tank! Moving cards to score pile...")
        self.show()

    def steal(self, card, opponent):
        color = card.frontColor
        opponentTankColors = [
            k for k, v in opponent.tank.items() if v > 0]
        if color in opponentTankColors:
            self.tank[color] += (opponent.tank[color] + 1)
            opponent.tank[color] = 0
            print(("{o} has {c} in their tank. "
                  "Steal successful :) moving to {s}'s tank...")
                  .format(o=opponent.name, c=color, s=self.name))
        else:
            opponent.tank[color] = 1
            print(("{o} doesn't have {c} in their tank. "
                  "Steal failed :( moving to {o}'s tank...")
                  .format(o=opponent.name, c=color, s=self.name))
        self.show()
        opponent.show()


if __name__ == "__main__":

    # Set seed for testing
    random.seed(123)

    # Define all available color options
    colorOptions = ['yellow', 'red', 'green',
                    'purple', 'blue', 'orange', 'pink']

    # Create players
    player1 = Player("Eric", colorOptions)
    player1.greet()
    player2 = Player("Amelia", colorOptions)
    player2.greet()
    print()

    # Simulate rounds for testing
    for i in range(10):
        # Draw a random card
        print(player1.name + " draws a card...")
        drawnCard = Card(colorOptions)
        drawnCard.showBothSides()

        # Player1 chooses to score
        print(player1.name + " chooses to score...")
        player1.score(drawnCard)
        # player1.show()
        print()

        # Draw a random card
        print(player2.name + " draws a card...")
        drawnCard = Card(colorOptions)
        drawnCard.showBothSides()

        # Player2 chooses to score
        print(player2.name + " chooses to score...")
        player2.score(drawnCard)
        # player2.show()
        print()

        # Draw a random card
        print(player1.name + " draws a card...")
        drawnCard = Card(colorOptions)
        drawnCard.showBothSides()

        # Player1 chooses to steal
        print(player1.name + " chooses to steal...")
        player1.steal(drawnCard, player2)
        # player1.show()
        print()
