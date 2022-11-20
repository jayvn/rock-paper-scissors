class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.move = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def add_score(self):
        self.score += 1


def get_winner(player1, player2):
    if player1.move == player2.move:
        return None

    if player1.move == "Rock":
        if player2.move == "Scissors":
            return player1
        else:
            return player2

    if player1.move == "Paper":
        if player2.move == "Rock":
            return player1
        else:
            return player2

    if player1.move == "Scissors":
        if player2.move == "Paper":
            return player1
        else:
            return player2


def parse_move_string(trigger):
    if trigger.endswith('rock'):
        return "Rock"
    elif trigger.endswith('paper'):
        return "Paper"
    elif trigger.endswith('scissors'):
        return "Scissors"
