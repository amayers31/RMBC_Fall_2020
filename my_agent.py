#!/usr/bin/env python3

"""
File Name:      my_agent.py
Authors:        Austin Ayers
Date:           10/31/20

Description:    Python file for my agent.
Source:         Adapted from recon-chess (https://pypi.org/project/reconchess/)
"""

import random
import chess
from datetime import datetime                   # Used to MCTS in a certain amount so we don't run
                                                # out of time
from player import Player


# TODO: Rename this class to what you would like your bot to be named during the game.
class Ayers(Player):

    def __init__(self):
        # Use the init to set up ways to keep track of the things the board knows
        self.board = None
        self.color = None
        
        # Set up a way to see if the opponent took one of your pieces, to immediately
        # respond since the strat should immediately respond to fire with fire
        self.taken_square = None

        # Set up a turn counter for the model so that we can make specific moves the first few turns
        self.turn_number = None
        
    def handle_game_start(self, color, board):
        """
        This function is called at the start of the game.

        :param color: chess.BLACK or chess.WHITE -- your color assignment for the game
        :param board: chess.Board -- initial board state
        :return:
        """
        # Preliminary implementation to handle the 
        self.board = board
        self.color = color
        self.turn_number = 0
        
    def handle_opponent_move_result(self, captured_piece, captured_square):
        """
        This function is called at the start of your turn and gives you the chance to update your board.

        :param captured_piece: bool - true if your opponents captured your piece with their last move
        :param captured_square: chess.Square - position where your piece was captured
        """
        # If a piece was captured then set the taken square to equal the captured square
        if captured_piece == True:
            # Set the self variable
            self.taken_square = captured_square
            # Alter the board that the player has in it's brain to see if 
            self.board.remove_piece_at(captured_square)

    def choose_sense(self, possible_sense, possible_moves, seconds_left):
        """
        This function is called to choose a square to perform a sense on.

        :param possible_sense: List(chess.SQUARES) -- list of squares to sense around
        :param possible_moves: List(chess.Moves) -- list of acceptable moves based on current board
        :param seconds_left: float -- seconds left in the game

        :return: chess.SQUARE -- the center of 3x3 section of the board you want to sense
        :example: choice = chess.A1
        """
        # TODO: update this method
        return random.choice(possible_sense)
        
    def handle_sense_result(self, sense_result):
        """
        This is a function called after your picked your 3x3 square to sense and gives you the chance to update your
        board.

        :param sense_result: A list of tuples, where each tuple contains a :class:`Square` in the sense, and if there
                             was a piece on the square, then the corresponding :class:`chess.Piece`, otherwise `None`.
        :example:
        [
            (A8, Piece(ROOK, BLACK)), (B8, Piece(KNIGHT, BLACK)), (C8, Piece(BISHOP, BLACK)),
            (A7, Piece(PAWN, BLACK)), (B7, Piece(PAWN, BLACK)), (C7, Piece(PAWN, BLACK)),
            (A6, None), (B6, None), (C8, None)
        ]
        """
        # Hint: until this method is implemented, any senses you make will be lost.
        # Rudimentary implementation to set pieces in the board that we have access to
        # Update the self.board with the observation by iterating over the list given in the sense result
        for square in sense_result:
            self.board.set_piece_at(square[0], square[1])

    def choose_move(self, possible_moves, seconds_left):
        """
        Choose a move to enact from a list of possible moves.

        :param possible_moves: List(chess.Moves) -- list of acceptable moves based only on pieces
        :param seconds_left: float -- seconds left to make a move
        
        :return: chess.Move -- object that includes the square you're moving from to the square you're moving to
        :example: choice = chess.Move(chess.F2, chess.F4)
        
        :condition: If you intend to move a pawn for promotion other than Queen, please specify the promotion parameter
        :example: choice = chess.Move(chess.G7, chess.G8, promotion=chess.KNIGHT) *default is Queen
        """
        # TODO: update this method -- Need to implement MCTS here
        choice = random.choice(possible_moves)
        return choice
        
    def handle_move_result(self, requested_move, taken_move, reason, captured_piece, captured_square):
        """
        This is a function called at the end of your turn/after your move was made and gives you the chance to update
        your board.

        :param requested_move: chess.Move -- the move you intended to make
        :param taken_move: chess.Move -- the move that was actually made
        :param reason: String -- description of the result from trying to make requested_move
        :param captured_piece: bool - true if you captured your opponents piece
        :param captured_square: chess.Square - position where you captured the piece
        """
        # TODO: implement this method
        pass
        
    def handle_game_end(self, winner_color, win_reason):  # possible GameHistory object...
        """
        This function is called at the end of the game to declare a winner.

        :param winner_color: Chess.BLACK/chess.WHITE -- the winning color
        :param win_reason: String -- the reason for the game ending
        """
        # TODO: implement this method
        pass

class Chess_Node:
    def __init__(self, board=None):
        # Set variables that will define the :
        # Set the board (Essentially what defines the node)
        self.board = board              # Will be a chess.Board board

        # Initialize the number of times the node has been visited when traversal occurs 
        # for the UCT calculations
        self.visits = None              # Will be an integer

        # Initialize the reward for the 
        self.reward = None              # Will be an integer

        # Set up variables so children are accessable and a parent is accessable
        self.parent = None              # Will be a single node
        self.children = None            # Will be a dictionary

    def __eq__(self, other):
        """
        Custom equality function for the Chess_Node to see if one node is equivalent to one 
        another

        :param other: The other node that is being compared to this one
        """
        # Two nodes are "equal" in our game universe if they have the same board 
        return self.board == other.board

    def __hash__(self):
        """
        Custom hash function for the Chess_Node to create 
        """
        return (hash(self.board))

    def analyze_board_w_fish(self, board, limit_time = 0.01):
        """
        Pulled this code from stack overflow because I didn't know how to used the 
        stockfish library

        :param board: The board that will be evaluated
        :param limit_time: The time limit that will be given for the evaluation
        """
        engine = chess.engine.SimpleEngine.popen_uci("stockfish_10_x64")
        result = engine.analyse(board, chess.engine.Limit(time=limit_time))
        return result['score']
