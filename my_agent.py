#!/usr/bin/env python3

"""
File Name:      my_agent.py
Authors:        TODO: Your names here!
Date:           TODO: The date you finally started working on this.

Description:    Python file for my agent.
Source:         Adapted from recon-chess (https://pypi.org/project/reconchess/)
"""

import random
import chess
from player import Player
from datetime import datetime


# TODO: Rename this class to what you would like your bot to be named during the game.
class MyAgent(Player):

    def __init__(self):
        pass
        
    def handle_game_start(self, color, board):
        """
        This function is called at the start of the game.

        :param color: chess.BLACK or chess.WHITE -- your color assignment for the game
        :param board: chess.Board -- initial board state
        :return:
        """"""
File Name:      my_agent.py
Authors:        Austin Ayers, Oscar Liu, Chanelleah Miller
Date:           10/31/20
Description:    Python file for my agent.
Source:         Adapted from recon-chess (https://pypi.org/project/reconchess/)
"""

import random
import chess
import chess.engine
from datetime import datetime                   # Used to MCTS in a certain amount so we don't run out of time

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

        #from https://python-chess.readthedocs.io/en/latest/engine.html
        self.engine = chess.engine.SimpleEngine.popen_uci("STOCKFISH_PATH_HERE")
        
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
        # if our piece was just captured, sense where it was captured
        if self.taken_square:
            return self.taken_square

        # if we might capture a piece when we move, sense where the capture will occur
        future_move = self.choose_move(possible_moves, seconds_left)
        if future_move is not None and self.board.piece_at(future_move.to_square) is not None:
            return future_move.to_square

        # otherwise, just randomly choose a sense action, but don't sense on a square where our pieces are located
        for square, piece in self.board.piece_map().items():
            if piece.color == self.color:
                possible_sense.remove(square)
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
        # if a move was executed, apply it to our board
        if taken_move is not None:
            self.board.push(taken_move)
        
    def handle_game_end(self, winner_color, win_reason):  # possible GameHistory object...
        """
        This function is called at the end of the game to declare a winner.
        :param winner_color: Chess.BLACK/chess.WHITE -- the winning color
        :param win_reason: String -- the reason for the game ending
        """
        # TODO: implement this method
        try:
            # if the engine is already terminated then this call will throw an exception
            self.engine.quit()
        except chess.engine.EngineTerminatedError:
            pass

	# function for node traversal 
    def expand(self, node):
        action = node.untried_actions.pop()
        child_board = 
        child_node = Chess_Node(child_board, parent = node)
        node.children.append(child_node)
        return child_node

    def uct(self, node):
            choices_weights = [
                (child.total_rewards / child.visits) + 1.4 * np.sqrt((2 * np.log(node.visits) / child.visits))
                for child in node.children
            ]
        return node.children[np.argmax(choices_weights)]

	def traverse(self, node):
		current = node
		while not #game_over:
			if not len(current.untried_actions)==0:
				return self.expand(current)
			else:
				current = self.uct(current)
	  	
	  	return current
	  

	# function for the result of the simulation 
	def rollout(self, node):
        curr_board = node.board 
	    while non_terminal(curr_board):
            move = possible_move(board)
            action = np.random.randint(len(move))
	        curr_board = curr_board.move(action) 
	    return result(curr_board) 
	  
	# function for backpropagation 
	def backpropagate(self, node, result): 
	    node.visits += 1
        node.result[result]+=1
	    	
	    if node.parent:
    	    self.backpropagate(node.parent, result) 

    def MCTS(self, possible_moves, seconds_left):
    	time = datetime.now()

    	root = Chess_Node(self.board)

    	while(hasTimeLeft()):
    		leaf = traverse(root)
    		simulation_result = rollout(leaf)
    		backpropagate(leaf, simulation _result)

    	return best_child_root

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

        # if we might be able to take the king, try to
        enemy_king_square = self.board.king(not self.color)
        if enemy_king_square:
            # if there are any ally pieces that can take king, execute one of those moves
            enemy_king_attackers = self.board.attackers(self.color, enemy_king_square)
            if enemy_king_attackers:
                attacker_square = enemy_king_attackers.pop()
                return chess.Move(attacker_square, enemy_king_square)

        # otherwise, try to move with the stockfish chess engine
        try:
            self.board.turn = self.color
            self.board.clear_stack()
            result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
            return result.move
        except chess.engine.EngineTerminatedError:
            print('Stockfish Engine died')
        except chess.engine.EngineError:
            print('Stockfish Engine bad state at "{}"'.format(self.board.fen()))

        # if all else fails, pass
        return None

class Chess_Node:
     def __init__(self, board=None, parent = None):
         self.board = board              # Will be a chess.Board board

         self.visits = 0              # Will be an integer

         # Initialize the reward for the
         self.result = defaultdict(int)              # Will be an integer

         self.untried_actions = None

         # Set up variables so children are accessable and a parent is accessable
         self.parent = parent            # Will be a single node
         self.children = []           # Will be a dictionary

     def total_rewards(self):
        wins = self.results[self.parent]
        loses = self.results[-1*self.parent]
        return wins - loses

     def untried_actions(self):
        if self.untried_actions is None:
            self.untried_actions = self.#possible_actions
     
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
        # TODO: implement this method
        pass

