#Author: Perrin Chhagan
#Date: 11/24/2020
#Description: This project uses three classes to replicate the board game Focus/Domination.
#There is the FocusGame class which contains the methods that should be called to play the game.
#There is is the Player class that represents the player and info specific to them.
#There is the Board_Location class that represents a board location and info specific to that spot.

class FocusGame:

    def __init__(self, player1, player2):
        '''This class will represent the overall game. It has method that
        allow for the game to be played. It will let a player make a move,
        show pieces at a given location, show a player's reserved or captured pieces
        and will announce when the game is won or drawn. It will interact
        with the player class and its methods to represent the players
        and manage their reserved and captured pieces. It will also interact
        with the board_location class to help manage which pieces are at any
        given location on the board.'''
        self._board = []

        for i in range(0,6):
            self._board.append([])
            for j in range(0, 6):
                if i % 2 == 0:
                    self._board[i].append(board_location(player1[1]))
                    if j == 2 or j == 3:
                        self._board[i][j] = board_location(player2[1])
                elif i % 2 != 0:
                    self._board[i].append(board_location(player2[1]))
                    if j == 2 or j == 3:
                        self._board[i][j] = board_location(player1[1])

        self._current = player1[0]
        self._player1 = Player(player1)
        self._player2 = Player(player2)



    def valid_move(self, player, source, destination, pieces):
        """
        This method will verify that a player is making a valid move,
        otherwise it will return an error. It will check to make sure the source and
        destination are on the board and a diagonal move is not being made.
        It will check to see whose turn it is.
        It will take the player making the move,
        the location to move pieces from and the location to move them to, and how many pieces
        to move as parameters.
        It will check to make sure the difference vertically or horizontally between the source and
        destination matches the number of pieces being moved.
        """
        player_obj = self.get_player(player)

        if self._current != player:
            return  False

        #checks to make sure source and destination are on the board
        for i in range(0,2):
            if source[i] < 0 or source[i] > 5 or destination[i] < 0 or destination[i] > 5:
                return False

        #checks to make sure player owns the stack they are trying to move
        if (self._board[source[0]][source[1]]).show_top_of_stack() != (player_obj.get_color()):
            return False

        #checks to make sure there are enough pieces to move
        if pieces > len((self._board[source[0]][source[1]]).get_pieces()):
            return False

        #checks to make sure number of spaces moved equals pieces moved
        if (abs(destination[0]-source[0])) != pieces and (abs(destination[1]-source[1])) != pieces:
            return False

        #checks to make sure diagonal move is not being made
        if (abs(source[0]) - abs(destination[0]) == 0) and source[1] != destination[1]:
            return "valid"
        elif (abs(source[1]) - abs(destination[1]) == 0) and source[0] != destination[0]:
            return "valid"
        else:
            return False



    def show_pieces(self, location):
        """This method will show the pieces at any given location on the board"""
        stack = (self._board[location[0]][location[1]]).get_pieces()
        return stack


    def move_piece(self, player, source,destination, pieces):
        """
        This method will allow a player to make a move. It will take the player making the move,
        the location to move pieces from and the location to move them to, and how many pieces
        to move as parameters. After a player makes a move, the self._current data member will
        be updated to show that it is now the opposite player's turn.
         """
        if self.valid_move(player, source, destination, pieces) != "valid":
            return self.valid_move(player, source, destination, pieces)

        #adds pieces to the destination
        (self._board[destination[0]][destination[1]]).add_pieces(pieces, (self._board[source[0]][source[1]]))

        #removes pieces from the source
        (self._board[source[0]][source[1]]).sub_pieces(pieces)

        #checks to see how tall destination stack is
        if len((self._board[destination[0]][destination[1]]).get_pieces()) > 5:
            self.tall_stack(destination, player)

        #checks for win
        if self.show_captured(player) == 6:
            return player + " Wins"

        #updates whose turn it is
        if player == self._player1.get_name():
            self._current = self._player2.get_name()
            return 'successfully moved'
        elif player == self._player2.get_name():
            self._current = self._player1.get_name()
            return 'successfully moved'

    def check_win(self, player):
        """
        Checks the board to see if the given player has won by checking the top color of every stack.
        Returns 1 if player has not won
        """
        for i in range(0, 6):
            for j in range(0, 6):
                if player != (self._board[i][j]).show_top_of_stack():
                    return 1


    def show_reserve(self,player):
        """Shows how many pieces are in a given player's reserve"""
        player = self.get_player(player)

        return player.get_reserve()

    def show_captured(self,player):
        """Shows how many pieces a given player has captured"""
        player = self.get_player(player)

        return player.get_capture()

    def reserved_move(self, player, destination):
        """
        This method will take a player's reserved piece, reduce their reserve count, and
        move it onto the board in the location given.
        Will return with a win statement if the player has won.
        """
        if self._current != player:
            return  'not your turn'

        for i in range(0,2):
            if destination[i] < 0 or destination[i] > 5:
                return 'invalid location'

        player_obj = self.get_player(player)

        if player_obj.get_reserve() == 0:
            return 'no pieces in reserve'

        player_obj.sub_reserve()

        (self._board[destination[0]][destination[1]]).add_reserve(player_obj)

        if self.show_captured(player)==6:
            return player + " Wins"


    def get_player(self, player):
        """Returns player object for given name"""
        if self._player1.get_name() == player:
            return self._player1
        elif self._player2.get_name() == player:
            return self._player2

    def tall_stack(self, destination, player):
        """
        This method will check if the stack at the given destination is greater than 5 pieces.
        If it is, it will cut down the stack and increment the proper player reserve and capture counts
        """

        length = len((self._board[destination[0]][destination[1]]).get_pieces())
        player_obj = self.get_player(player)
        list = (self._board[destination[0]][destination[1]]).get_pieces()

        while length > 5:
            if list[0] == player_obj.get_color():
                player_obj.add_reserve(1)
            else:
                player_obj.add_capture(1)
            (self._board[destination[0]][destination[1]]).remove_first()
            length = len((self._board[destination[0]][destination[1]]).get_pieces())

class Player:
    """
    This class represents a player and has methods to
    add or remove pieces from their reserve or add pieces that they have captured.
    It has methods to show their name, color, reserve count, and capture count.
    It will interact with the FocusGame class to help manage player info
    """

    def __init__(self, player):
        self._reserve = 0
        self._capture = 0
        self._name = player[0]
        self._color = player[1]

    def get_name(self):
        """Returns a player's name"""
        return self._name

    def get_color(self):
        """Returns a player's color"""
        return self._color

    def get_reserve(self):
        """Returns a player's reserve count"""
        return self._reserve

    def get_capture(self):
        """Returns a player's captured count"""
        return self._capture

    def add_reserve(self, total):
        """Adds a given amount to a player's reserve total """
        self._reserve += total

    def add_capture(self, total):
        """Adds a given amount to a player's reserve total"""
        self._capture += total

    def sub_reserve(self):
        """Reduces the player's reserve total"""
        self._reserve -= 1


class board_location:
    """
    This class represents a location on the board and adds or subtracts pieces.
    It will show which color is on the top of the stack. It interacts with the FocusGame
    class to help maintain which pieces are where and how many pieces are in a stack
    """

    def __init__(self, color):
        """Initializes the board location with a given color"""
        self._pieces = [color]

    def get_pieces(self):
        """Returns the amount of pieces for the location object"""
        return self._pieces

    def add_pieces(self, pieces, source):
        """Adds a given amount of pieces to a location's stack"""
        length = len(source.get_pieces())

        for i in range((length - pieces), length):
            self._pieces.append((source.get_pieces())[i])

    def add_reserve(self, player):
        """Adds a reserve piece with a given player's color"""
        self._pieces.append(player.get_color())

    def sub_pieces(self, pieces):
        """Removes a given amount of pieces from the stack"""
        length = len(self.get_pieces())

        for i in range(length - 1, (length - pieces) - 1, -1):
            del self._pieces[-1]

    def show_top_of_stack(self):
        """shows the color on top of the stack"""
        length = len(self._pieces)

        if length == 0:
            return False
        else:
            return str(self._pieces[length-1])

    def remove_first(self):
        """Removes the first piece of the stack"""
        del self._pieces[0]
