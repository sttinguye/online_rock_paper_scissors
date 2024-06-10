class Game:
    def __init__(self, id):
        self.p1Went = False  # / if player 1 has made a move or not
        self.p2Went = False  # / if player 2 has made a move or not
        self.ready = False  # / if both player have made a move or not
        self.id = id  # / current game id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0
        self.NAMES = [None, None]

    def get_player_name(self,names, p):  # get player name
        self.NAMES[p] = names
        return self.names[p]  # return the name of player

    def get_player_move(self, p):  # get player move
        """
        :param p: [0,1]
        :return:Move
        """
        return self.moves[p]  # return the move of player

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True  # keep track of if we move or not
        else:
            self.p2Went = True

    def connected(self):
        return self.ready # check if the players ready or not

    def bothWent(self):
        return self.p1Went and self.p2Went # check if the players both went or not

    #def return_name(self, name, p):
        #self.Name[p] = name[17:]
        #return self.Name[p]

    def winner(self):
        p1 = self.moves[0].upper()[0] # get the first letter of the move
        p2 = self.moves[1].upper()[0] # get the first letter of the move

        winner = -1 # because it could be a tie
        if p1 == "R" and p2 == "S":
            winner = 0 # p1 win
        elif p1 == "S" and p2 == "R":
            winner = 1 # p2 win
        elif p1 == "P" and p2 == "R":
            winner = 0 # p1 win
        elif p1 == "R" and p2 == "P":
            winner = 1 # p2 win
        elif p1 == "S" and p2 == "P":
            winner = 0 # p1 win
        elif p1 == "P" and p2 == "S":
            winner = 1 # p2 win

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
