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

        self.sq = {}
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
        #future_move = self.choose_move(possible_moves, seconds_left)
        #if future_move is not None and self.board.piece_at(future_move.to_square) is not None:
        #    return future_move.to_square

        # otherwise, just randomly choose a sense action, but don't sense on a square where our pieces are located
        for square, piece in self.board.piece_map().items():
            if (piece.color == self.color and not piece.piece_type == chess.KING and not piece.piece_type == chess.QUEEN):
                possible_sense.remove(square)

        for s in range(64):
            if s<8 or s > 55 or s%8==0 or s%8==7:
                if s in possible_sense:
                    possible_sense.remove(s)
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
        self.sq = {}
        for square in sense_result:
            self.board.set_piece_at(square[0], square[1])
            if not square[1] is None and not square[1].color == self.color:
                piece_type = square[1].piece_type
                if not piece_type in self.sq:
                    self.sq[piece_type] = [square[0]]
                else:
                    self.sq[piece_type].append(square[0])



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
        self.board.push(taken_move if taken_move is not None else chess.Move.null())
        
    def handle_game_end(self, winner_color, win_reason):  # possible GameHistory object...
        """
        This function is called at the end of the game to declare a winner.
        :param winner_color: Chess.BLACK/chess.WHITE -- the winning color
        :param win_reason: String -- the reason for the game ending
        """
        # TODO: implement this method
        pass

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
    
        for piece in range(6,0,-1):
            if piece in self.sq:
                for e in self.sq[piece]:
                    enemy_attackers = self.board.attackers(self.color, e)
                    if enemy_attackers:
                        i = 7
                        attacker = None
                        for attackers in enemy_attackers:
                            index = self.board.piece_at(attackers).piece_type
                            if index < i:
                                i = index
                                attacker = attackers
                        if i <= piece+1:
                            return chess.Move(attacker, e)

        # if all else fails, pass
        self.board.turn = self.color
        M = MCTS(self.board, self.color, possible_moves, seconds_left)

        print(seconds_left)
        action = M.Search()
        if action is None:
            return possible_moves[np.random.randint((int)(len(possible_moves)/2))]
        return action

class MCTS:
    def __init__(self, board, color, possible_moves, seconds_left):
        self.root = Chess_Node(board, color)
        self.possible_moves = possible_moves
        self.seconds_left = seconds_left

    def traverse(self):
        current = self.root
        while not current is None and not current.is_over():
            if not len(current.untried_actions)==0:
                child = current.expand()
                if not child is None:
                    return child
                else:
                    current = current.uct()
            else:
                current = current.uct()

        return None

    def Search(self):
        time = datetime.now()

        count = 0
        count_None = 0
        while(count < 100):
            leaf = self.traverse()
            if leaf is None: 
                break
            simulation_result = leaf.rollout()
            leaf.backpropagate(simulation_result)
     
            count =  count + 1

        child = self.root.uct(param = 0.0)
        if child is None:
            return None
        return child.action
        

class Chess_Node:
    def __init__(self, board, color, parent = None):
        self.board = board              # Will be a chess.Board board
        self.color =  color
        self.board.turn = color
        self.total_rewards = 0
        self.visits = 0      
        self.parent = parent

        self.untried_actions = self.possible()

        # Set up variables so children are accessable and a parent is accessable
        self.children = []           
        self.action = None

    def is_over(self):
        return self.board.king(chess.WHITE) is None or self.board.king(chess.BLACK) is None

    def _add_pawn_queen_promotion(self, move):
        back_ranks = list(chess.SquareSet(chess.BB_BACKRANKS))
        piece = self.board.piece_at(move.from_square)
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

    def _revise_move(self, move):
        # if its a legal move, don't change it at all. note that board.generate_psuedo_legal_moves() does not
        # include psuedo legal castles
        if move in self.board.generate_pseudo_legal_moves() or self._is_psuedo_legal_castle(self.board, move):
            return move

        # note: if there are pieces in the way, we DONT capture them
        if self._is_illegal_castle(self.board, move):
            return None

        # if the piece is a sliding piece, slide it as far as it can go
        piece = self.board.piece_at(move.from_square)
        if not piece is None and piece.piece_type in [chess.PAWN, chess.ROOK, chess.BISHOP, chess.QUEEN]:
            move = self._slide_move(self.board, move)

        return move if move in self.board.generate_pseudo_legal_moves() else None

    def check_move(self, requested_move):
        """
        Takes in the agent requested move and updatest he board accordingly with any possible rule revision
        :param requested_move: chess.Move -- the move the agent requested
        
        :return requested_move: chess.Move -- the move the agent requested
        :return taken_move: chess.Move -- the move that was actually taken 
        :return captured_square: chess.SQUARE -- the square where an opponent's piece is captured
                                 None -- if there is no captured piece
        """
        if self.is_over():
            return False

        move = self._add_pawn_queen_promotion(requested_move)
        taken_move = self._revise_move(move)
        
        return (taken_move is not None)

    # function for node traversal 
    def expand(self):
        while len(self.untried_actions)>0:
            action = self.untried_actions.pop()
            if self.check_move(action):
                curr_board = self.board.copy()
                curr_board.push(action)
                child_node = Chess_Node(curr_board, (not self.color), parent = self)
                child_node.action = action
                self.children.append(child_node)
                return child_node

        return None


    def uct(self, param = 1.4):
        choices_weights = [
            (child.total_rewards / child.visits) + param * np.sqrt((2 * np.log(self.visits) / child.visits)) 
            for child in self.children
        ]
        
        if len(choices_weights)==0:
            return None
        
        return self.children[np.argmax(choices_weights)]
      
    def result(self):
        if not self.is_over():
            return 0
        if self.color == chess.WHITE:
            if self.board.king(chess.WHITE) is None:
                return -1
            else:
                return 1
        else:
            if self.board.king(chess.BLACK) is None:
                return -1
            else:
                return 1

    def handle_move(self, move):
        self.board.push(move)

    def handle_turn(self):
        self.color = not (self.color)
        self.board.turn = self.color

    # function for the result of the simulation 
    def rollout(self):
        curr_board = self.board.copy()
        curr_node = Chess_Node(curr_board, self.color)
        count = 0
        while not curr_node.is_over() and count < 100:
            move = curr_node.possible()
            if len(move) == 0: 
                return curr_node.result()
            action = np.random.randint(len(move))
            curr_change = curr_node.check_move(move[action])
            if curr_change:
                curr_node.handle_move(move[action])
            curr_node.handle_turn()
            count = count + 1
        return curr_node.result() 

    # function for backpropagation 
    def backpropagate(self, result): 
        self.visits += 1
        self.total_rewards+=result
            
        if self.parent:
            self.parent.backpropagate(result)

    def possible(self):
        b = self.board.copy()
        for piece_type in chess.PIECE_TYPES:
            for sq in b.pieces(piece_type, not self.color):
                b.remove_piece_at(sq)

        pawn_capture_moves = []

        no_opponents_board = b.copy()

        for pawn_square in self.board.pieces(chess.PAWN, self.color):
            for attacked_square in self.board.attacks(pawn_square):
                # skip this square if one of our own pieces are on the square
                if no_opponents_board.piece_at(attacked_square):
                    continue

                pawn_capture_moves.append(chess.Move(pawn_square, attacked_square))

                # add in promotion moves
                if attacked_square in chess.SquareSet(chess.BB_BACKRANKS):
                    for piece_type in chess.PIECE_TYPES[1:-1]:
                        pawn_capture_moves.append(chess.Move(pawn_square, attacked_square, promotion=piece_type))

        return list(b.generate_pseudo_legal_moves()) + pawn_capture_moves



