import random
import time
import argparse


class Die:
    "Numbered cube"

    def __init__(self, seed=0):
        random.seed(seed)

    def roll(self):
        return random.randint(1, 6)


class Player:
    "A Player in the game of Pig"

    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

    def decides_to_roll(self, turn_score):
        choice = input(f"{self.name}, Roll or hold? (r/h) ").lower()
        return choice == 'r'


class ComputerPlayer(Player):
    "Computer decides to roll"

    def decides_to_roll(self, turn_total):
        "Computer rolls until reaching 25 or close to 100"
        target = min(25, 100 - self.score)
        return turn_total < target


class PlayerFactory:
    "Factory to create players"

    def create_player(self, player_type, name):
        if player_type == "computer":
            return ComputerPlayer(name)
        return Player(name)


class Game:

    def __init__(self, player1, player2):
        self.die = Die()
        self.players = [player1, player2]
        self.current_player = 0

    def switch_turn(self):
        self.current_player = 1 - self.current_player

    def play_turn(self):
        player = self.players[self.current_player]
        turn_total = 0

        print(f"\n{player.name}'s turn. Current Score: {player.score}")

        while True:
            roll = self.die.roll()
            print(f"{player.name} rolled: {roll}")

            if roll == 1:
                print(f"{player.name} loses all points this turn!")
                turn_total = 0
                break
            else:
                turn_total += roll
                print(f"Turn total: {turn_total}, Game score: {player.score}")

                if not player.decides_to_roll(turn_total):
                    break

        player.add_score(turn_total)
        print(f"{player.name}'s new score: {player.score}")
        self.switch_turn()

    def is_winner(self, player):
        return player.score >= 100

    def play_game(self):
        while True:
            self.play_turn()
            if self.is_winner(self.players[self.current_player - 1]):
                print(f"{self.players[self.current_player - 1].name} wins with {self.players[self.current_player - 1].score} points!")
                break


class Proxy:
    "Proxy to implement timed version of the game"

    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def play_game(self):
        while True:
            if time.time() - self.start_time > 60:
                print("\nTime's up! Determining winner...")
                self.declare_winner()
                break

            self.game.play_turn()
            if self.game.is_winner(self.game.players[self.game.current_player - 1]):
                print(f"{self.game.players[self.game.current_player - 1].name} wins with {self.game.players[self.game.current_player - 1].score} points!")
                break

    def declare_winner(self):
        scores = {player.name: player.score for player in self.game.players}
        winner = max(scores, key=scores.get)
        print(f"{winner} wins with {scores[winner]} points!")
        time.sleep(2)


def main():
    "Main function to handle player creation and start the game"

    parser = argparse.ArgumentParser()
    parser.add_argument('--player1', choices=['human', 'computer'], default='human', help='Player 1 type')
    parser.add_argument('--player2', choices=['human', 'computer'], default='computer', help='Player 2 type')
    parser.add_argument('--timed', action='store_true', help='Enable timed game (1-minute limit)')

    args = parser.parse_args()

    factory = PlayerFactory()

 
    player1 = factory.create_player(args.player1, "Player 1")
    player2 = factory.create_player(args.player2, "Player 2")

    game = Game(player1, player2)

    if args.timed:
        game_proxy = Proxy(game)
        game_proxy.play_game()
    else:
        game.play_game()


if __name__ == "__main__":
    main()
