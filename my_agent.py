  
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
import numpy as np
from collections import defaultdict
from datetime import datetime

'''
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
        """
'''
"""
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


def possible_moves(board, color):
    ## This is lifted from game.py
    # Will return a list of valid moves
    # Get the board without opponnets pieces
    b = board.copy()
    for piece_type in chess.PIECE_TYPES:
        for sq in b.pieces(piece_type, not color):
            b.remove_piece_at(sq)

    pawn_capture_moves = []

    no_opponents_board = b

    for pawn_square in board.pieces(chess.PAWN, self.color):
        for attacked_square in board.attacks(pawn_square):
            # skip this square if one of our own pieces are on the square
            if no_opponents_board.piece_at(attacked_square):
                continue

            pawn_capture_moves.append(chess.Move(pawn_square, attacked_square))

            # add in promotion moves
            if attacked_square in chess.SquareSet(chess.BB_BACKRANKS):
                for piece_type in chess.PIECE_TYPES[1:-1]:
                    pawn_capture_moves.append(chess.Move(pawn_square, attacked_square, promotion=piece_type))

    return list(b.generate_psudo_legal_moves()) + pawn_capture_moves

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
        #self.engine = chess.engine.SimpleEngine.popen_uci("STOCKFISH_PATH_HERE")
        
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

    def is_over(self, board):
        return board.king(chess.WHITE) is None or board.king(chess.BLACK) is None

    def _add_pawn_queen_promotion(self, board, move):
        back_ranks = list(chess.SquareSet(chess.BB_BACKRANKS))
        piece = board.piece_at(move.from_square)
        if piece is not None and piece.piece_type == chess.PAWN and move.to_square in back_ranks and move.promotion is None:
            move = chess.Move(move.from_square, move.to_square, chess.QUEEN)
        return move
    
    def _is_psuedo_legal_castle(self, board, move):
        return board.is_castling(move) and not self._is_illegal_castle(board, move)
    
    def _is_illegal_castle(self, board, move):
        if not board.is_castling(move):
            return False

        # illegal without kingside rights
        if board.is_kingside_castling(move) and not board.has_kingside_castling_rights(board.turn):
            return True

        # illegal without queenside rights
        if board.is_queenside_castling(move) and not board.has_queenside_castling_rights(board.turn):
            return True

        # illegal if any pieces are between king & rook
        rook_square = chess.square(7 if board.is_kingside_castling(move) else 0, chess.square_rank(move.from_square))
        between_squares = chess.SquareSet(chess.BB_BETWEEN[move.from_square][rook_square])
        if any(map(lambda s: board.piece_at(s), between_squares)):
            return True

        # its legal
        return False
    
    def _slide_move(self, board, move):
        psuedo_legal_moves = list(board.generate_pseudo_legal_moves())
        squares = list(chess.SquareSet(chess.BB_BETWEEN[move.from_square][move.to_square])) + [move.to_square]
        squares = sorted(squares, key=lambda s: chess.square_distance(s, move.from_square), reverse=True)
        for slide_square in squares:
            revised = chess.Move(move.from_square, slide_square, move.promotion)
            if revised in psuedo_legal_moves:
                return revised
        return None

    def _revise_move(self, board, move):
        # if its a legal move, don't change it at all. note that board.generate_psuedo_legal_moves() does not
        # include psuedo legal castles
        if move in board.generate_pseudo_legal_moves() or self._is_psuedo_legal_castle(board, move):
            return move

        # note: if there are pieces in the way, we DONT capture them
        if self._is_illegal_castle(board, move):
            return None

        # if the piece is a sliding piece, slide it as far as it can go
        piece = board.piece_at(move.from_square)
        if piece.piece_type in [chess.PAWN, chess.ROOK, chess.BISHOP, chess.QUEEN]:
            move = self._slide_move(board, move)

        return move if move in self.truth_board.generate_pseudo_legal_moves() else None

    def handle_move(self, board, requested_move):
        """
        Takes in the agent requested move and updatest he board accordingly with any possible rule revision
        :param requested_move: chess.Move -- the move the agent requested
        
        :return requested_move: chess.Move -- the move the agent requested
        :return taken_move: chess.Move -- the move that was actually taken 
        :return captured_square: chess.SQUARE -- the square where an opponent's piece is captured
                                 None -- if there is no captured piece
        """
        move = self._add_pawn_queen_promotion(board, requested_move)
        taken_move = self._revise_move(board, move)
        
        # push move to appropriate boards for updates #
        board.push(taken_move if taken_move is not None else chess.Move.null())
        return board

    # function for node traversal 
    def expand(self, node):
        action = node.untried_actions.pop()
        child_board = self.handle_move(node.board, action)
        child_node = Chess_Node(child_board, parent = node, )
        child_node.action = action
        node.children.append(child_node)
        return child_node

    def uct(self, node, param = 1.4):
        choices_weights = [
            (child.total_rewards / child.visits) + param * np.sqrt((2 * np.log(node.visits) / child.visits))
            for child in node.children
        ]
        return node.children[np.argmax(choices_weights)]


    def traverse(self, node):
        current = node
        while not self.is_over(current):
            if not len(current.untried_actions)==0:
                return self.expand(current)
            else:
                current = self.uct(current)
        
        return current
      
    def result(self, board):
        if not self.is_over(board):
            return 0
        if self.color == chess.WHITE:
            if board.king(chess.WHITE) is None:
                return -1
            else:
                return 1
        else:
            if board.king(chess.BLACK) is None:
                return -1
            else:
                return 1

    # function for the result of the simulation 
    def rollout(self, node):
        curr_board = node.board.copy()
        count = 0
        while not self.is_over(cur_board) and count < 500:
            move = possible_moves(cur_board)
            action = np.random.randint(len(move))
            curr_board = self.handle_move(curr_board, action) 
            count = count + 1
        return self.result(curr_board) 
      
    # function for backpropagation 
    def backpropagate(self, node, result): 
        node.visits += 1
        node.result[result]+=1
            
        if node.parent:
            self.backpropagate(node.parent, result) 

    def MCTS(self, possible_moves, seconds_left):
        time = datetime.now()

        root = Chess_Node(self.board)

        while(datetime.now()-time < seconds_left-1):
            leaf = self.traverse(root)
            simulation_result = self.rollout(leaf)
            self.backpropagate(leaf, simulation_result)

        return root.uct(param = 0.0).action

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
        '''
        try:
            self.board.turn = self.color
            self.board.clear_stack()
            result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
            return result.move
        except chess.engine.EngineTerminatedError:
            print('Stockfish Engine died')
        except chess.engine.EngineError:
            print('Stockfish Engine bad state at "{}"'.format(self.board.fen()))
        '''

        # if all else fails, pass
        return self.MCTS(possible_moves, seconds_left)
        

class Chess_Node:
     def __init__(self, board=None, color, parent = None):
         self.board = board              # Will be a chess.Board board
         self.color =  color

         self.visits = 0              # Will be an integer

         # Initialize the reward for the
         self.result = defaultdict(int)              # Will be an integer

         self.untried_actions = possible_moves(self.board, self.color)

         # Set up variables so children are accessable and a parent is accessable
         self.parent = parent            # Will be a single node
         self.children = []           # Will be a dictionary
         self.action = None

     def total_rewards(self):
        wins = self.results[self.parent]
        loses = self.results[-1*self.parent]
        return wins - loses
     
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
     '''
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
    '''