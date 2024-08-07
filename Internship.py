import sys
import random

class MarbleGame:
    def __init__(self, red, blue, version='standard', first_player='computer', depth=None):
        self.initial_red = red
        self.initial_blue = blue
        self.red = red
        self.blue = blue
        self.version = version
        self.current_player = first_player
        self.depth = depth if depth is not None else float('inf')
        self.game_over = False
        self.human_score = 0
        self.computer_score = 0

    def is_game_over(self):
        if self.red == 0 or self.blue == 0:
            self.game_over = True
        return self.game_over

    def get_score(self):
        return self.red * 2 + self.blue * 3

    def get_moves(self):
        moves = []
        if self.red >= 2:
            moves.append((2, 0))
        if self.blue >= 2:
            moves.append((0, 2))
        if self.red >= 1:
            moves.append((1, 0))
        if self.blue >= 1:
            moves.append((0, 1))
        return moves

    def make_move(self, move):
        r, b = move
        self.red -= r
        self.blue -= b

    def undo_move(self, move):
        r, b = move
        self.red += r
        self.blue += b

    def evaluate(self):
        if self.version == 'standard':
            if self.red == 0 or self.blue == 0:
                return -1 if self.current_player == 'human' else 1
        elif self.version == 'misere':
            if self.red == 0 or self.blue == 0:
                return 1 if self.current_player == 'human' else -1
        return 0

    def minmax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over():
            return self.evaluate()
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_moves():
                self.make_move(move)
                eval = self.minmax(depth - 1, alpha, beta, False)
                self.undo_move(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_moves():
                self.make_move(move)
                eval = self.minmax(depth - 1, alpha, beta, True)
                self.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def best_move(self):
        best_move = None
        best_value = float('-inf') if self.current_player == 'computer' else float('inf')
        for move in self.get_moves():
            self.make_move(move)
            move_value = self.minmax(self.depth - 1, float('-inf'), float('inf'), self.current_player == 'human')
            self.undo_move(move)
            if (self.current_player == 'computer' and move_value > best_value) or \
               (self.current_player == 'human' and move_value < best_value):
                best_value = move_value
                best_move = move
        return best_move

    def play_game(self):
        while not self.is_game_over():
            if self.current_player == 'human':
                print(f"Current state: Red marbles = {self.red}, Blue marbles = {self.blue}")
                print("Available moves:", self.get_moves())
                
                while True:
                    try:
                        move_input = input("Enter your move (red blue): ")
                        move = tuple(map(int, move_input.split()))
                        if len(move) != 2:
                            raise ValueError("Input must be two integers separated by a space.")
                        if move not in self.get_moves():
                            raise ValueError("Invalid move. Try again.")
                        break  # Exit the loop if input is valid
                    except ValueError as e:
                        print(e)  # Print error message and prompt for input again
                
                self.make_move(move)
                self.current_player = 'computer'
            else:
                move = self.best_move()
                print(f"Computer moves: {move}")
                self.make_move(move)
                self.current_player = 'human'
        
        print("Game Over!")
        print(f"Remaining marbles: Red = {self.red}, Blue = {self.blue}")

        # Calculate final scores
        final_red = self.red
        final_blue = self.blue
        human_score = (self.initial_red - final_red) * 2 + (self.initial_blue - final_blue) * 3
        computer_score = (final_red) * 2 + (final_blue) * 3
        
        print(f"Final scores: Human = {human_score}, Computer = {computer_score}")

        # Determine the winner
        if human_score > computer_score:
            print("Winner: Human")
        elif computer_score > human_score:
            print("Winner: Computer")
        else:
            print("It's a tie!")

def parse_args(args):
    if len(args) < 5:
        raise ValueError("Usage: python marbles_game.py <num-red> <num-blue> <version> <first-player> [<depth>]")
    
    red = int(args[1])
    blue = int(args[2])
    version = args[3]
    first_player = args[4]
    depth = int(args[5]) if len(args) > 5 else None

    return red, blue, version, first_player, depth

def run_game(args):
    try:
        red, blue, version, first_player, depth = parse_args(args)
        game = MarbleGame(red, blue, version, first_player, depth)
        game.play_game()
    except ValueError as e:
        print(e)

# For Jupyter Notebook, manually set the parameters and run:
# Replace these values with desired ones
red = 5
blue = 7
version = 'standard'
first_player = 'human'
depth = 3

game = MarbleGame(red, blue, version, first_player, depth)
game.play_game()
