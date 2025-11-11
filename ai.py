"""AI opponent with multiple difficulty levels.

Hard/Impossible use a minimax search with alpha-beta pruning; easier levels
introduce strategic heuristics and occasional mistakes for a human feel.
"""

from typing import Optional, Tuple
import random
import time
from constants import BOARD_ROWS, BOARD_COLS


class AIPlayer:
    """Encapsulates move selection for the 'O' player."""

    def __init__(self, board, difficulty: str = "Hard"):
        self.board = board
        self.difficulty = difficulty
        self.max_depth = self._get_max_depth()
        self.mistake_probability = self._get_mistake_probability()
    
    def _get_max_depth(self) -> int:
        depth_map = {
            "Easy": 1,
            "Medium": 3,
            "Hard": 6,
            "Impossible": 9
        }
        return depth_map.get(self.difficulty, 9)
    
    def _get_mistake_probability(self) -> float:
        mistake_map = {
            "Easy": 0.4,
            "Medium": 0.15,
            "Hard": 0.05,
            "Impossible": 0.0
        }
        return mistake_map.get(self.difficulty, 0.0)
    
    def get_move(self, game_state) -> Optional[Tuple[int, int]]:
        """Return best (row, col) for current position; never mutates board."""
        if random.random() < self.mistake_probability:
            time.sleep(random.uniform(0.2, 0.4))
            return self._get_random_move(game_state)
        
        if self.difficulty == "Easy":
            time.sleep(random.uniform(0.2, 0.4))
            move = self._try_win_move(game_state)
            if move:
                return move
            if random.random() < 0.5:
                return self._get_random_move(game_state)
            else:
                return self._get_strategic_move(game_state)
        elif self.difficulty == "Medium":
            time.sleep(random.uniform(0.3, 0.5))
            move = self._try_win_move(game_state)
            if move:
                return move
            move = self._try_block_move(game_state)
            if move:
                return move
            return self._get_strategic_move(game_state)
        else:
            move = self._get_best_move(game_state)
            time.sleep(random.uniform(0.3, 0.6))
            return move
    
    def make_move(self, game_state) -> None:
        """Mutating variant for convenience in simpler call sites."""
        move = self.get_move(game_state)
        if move:
            game_state.board[move[0]][move[1]] = "O"
    
    def _make_random_move(self, game_state) -> None:
        move = self._get_random_move(game_state)
        if move:
            game_state.board[move[0]][move[1]] = "O"
    
    def _get_random_move(self, game_state) -> Optional[Tuple[int, int]]:
        empty_cells = game_state.get_empty_cells()
        if empty_cells:
            return random.choice(empty_cells)
        return None
    
    def _get_best_move(self, game_state) -> Optional[Tuple[int, int]]:
        best_score = float('-inf')
        best_move = None
        
        board = game_state.board
        empty_cells = self._get_empty_cells(board)
        
        for row, col in empty_cells:
            temp_board = [r[:] for r in board]
            temp_board[row][col] = "O"
            
            temp_state = type('obj', (object,), {
                'board': temp_board,
                'is_board_full': lambda: self._is_board_full(temp_board),
                'get_empty_cells': lambda: self._get_empty_cells(temp_board)
            })()
            
            score = self._minimax(temp_state, 0, False, float('-inf'), float('inf'))
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move
    
    def _minimax(self, game_state, depth: int, is_maximizing: bool, alpha: float, beta: float) -> int:
        winner = self._check_winner(game_state.board)
        
        if winner == "O":
            return 10 - depth
        elif winner == "X":
            return depth - 10
        elif self._is_board_full(game_state.board):
            return 0
        
        if depth >= self.max_depth:
            return 0
        
        board = game_state.board
        
        if is_maximizing:
            max_score = float('-inf')
            empty_cells = self._get_empty_cells(board)
            for row, col in empty_cells:
                temp_board = [r[:] for r in board]
                temp_board[row][col] = "O"
                
                temp_state = type('obj', (object,), {'board': temp_board})()
                score = self._minimax(temp_state, depth + 1, False, alpha, beta)
                
                max_score = max(score, max_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = float('inf')
            empty_cells = self._get_empty_cells(board)
            for row, col in empty_cells:
                temp_board = [r[:] for r in board]
                temp_board[row][col] = "X"
                
                temp_state = type('obj', (object,), {'board': temp_board})()
                score = self._minimax(temp_state, depth + 1, True, alpha, beta)
                
                min_score = min(score, min_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score
    
    def _check_winner(self, board) -> Optional[str]:
        """Pure winner check for a provided board snapshot."""
        for row in range(BOARD_ROWS):
            if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
                return board[row][0]
        
        for col in range(BOARD_COLS):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
                return board[0][col]
        
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return board[0][0]
        
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return board[0][2]
        
        return None
    
    def _is_board_full(self, board) -> bool:
        return all(all(cell is not None for cell in row) for row in board)
    
    def _get_empty_cells(self, board) -> list:
        return [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] is None]
    
    def _try_win(self, game_state) -> bool:
        move = self._try_win_move(game_state)
        if move:
            game_state.board[move[0]][move[1]] = "O"
            return True
        return False
    
    def _try_win_move(self, game_state) -> Optional[Tuple[int, int]]:
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if game_state.board[r][c] is None:
                    game_state.board[r][c] = "O"
                    if self._check_winner(game_state.board) == "O":
                        game_state.board[r][c] = None
                        return (r, c)
                    game_state.board[r][c] = None
        return None
    
    def _try_block(self, game_state) -> bool:
        move = self._try_block_move(game_state)
        if move:
            game_state.board[move[0]][move[1]] = "O"
            return True
        return False
    
    def _try_block_move(self, game_state) -> Optional[Tuple[int, int]]:
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if game_state.board[r][c] is None:
                    game_state.board[r][c] = "X"
                    if self._check_winner(game_state.board) == "X":
                        game_state.board[r][c] = None
                        return (r, c)
                    game_state.board[r][c] = None
        return None
    
    def _make_strategic_move(self, game_state) -> None:
        move = self._get_strategic_move(game_state)
        if move:
            game_state.board[move[0]][move[1]] = "O"
    
    def _get_strategic_move(self, game_state) -> Optional[Tuple[int, int]]:
        if game_state.board[1][1] is None:
            return (1, 1)
        
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        empty_corners = [(r, c) for r, c in corners if game_state.board[r][c] is None]
        if empty_corners:
            return random.choice(empty_corners)
        
        empty_cells = game_state.get_empty_cells()
        if empty_cells:
            return random.choice(empty_cells)
        
        return None
