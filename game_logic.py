"""Core game domain logic: board state, win detection, statistics.

Keeping this module free of any rendering or event-loop details helps testability
and makes the AI and UI layers depend on a stable, minimal API.
"""

from typing import Optional, List, Tuple
import time

from constants import BOARD_ROWS, BOARD_COLS, WIDTH


class GameState:
    """Mutable game session state for a single Tic-Tac-Toe round."""

    def __init__(self) -> None:
        # 3x3 board; None means empty, otherwise 'X' or 'O'
        self.board: List[List[Optional[str]]] = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.player: str = "X"  # current player symbol
        self.game_over: bool = False
        self.winner: Optional[str] = None
        self.winning_line: Optional[Tuple[int, int, int, int]] = None  # pixel coordinates for highlight
        # Simple timing accumulation (could be extended for per-move analytics)
        self.move_start_time: float = time.time()
        self.player_time: float = 0.0
        self.ai_time: float = 0.0

    def reset(self) -> None:
        """Clear board and timing, preparing for a new round."""
        self.board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.player = "X"
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.move_start_time = time.time()
        self.player_time = 0.0
        self.ai_time = 0.0

    def make_move(self, row: int, col: int) -> bool:
        """Place current player's symbol if target cell is empty.

        Returns True on success, False if the move is invalid or cell occupied.
        """
        if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS and self.board[row][col] is None:
            move_time = time.time() - self.move_start_time
            if self.player == "X":
                self.player_time += move_time
            else:
                self.ai_time += move_time
            self.board[row][col] = self.player
            self.move_start_time = time.time()
            return True
        return False

    def check_winner(self) -> Optional[str]:
        """Evaluate board for a winner, storing highlight line if found."""
        cell_span = WIDTH // BOARD_COLS
        for row in range(BOARD_ROWS):
            a, b, c = self.board[row]
            if a is not None and a == b == c:
                y = row * cell_span + cell_span // 2
                self.winning_line = (20, y, WIDTH - 20, y)
                return a

        for col in range(BOARD_COLS):
            a = self.board[0][col]
            if a is not None and a == self.board[1][col] == self.board[2][col]:
                x = col * cell_span + cell_span // 2
                self.winning_line = (x, 20, x, cell_span * BOARD_ROWS - 20)
                return a

        center = self.board[1][1]
        if center is not None:
            # main diagonal
            if self.board[0][0] == center == self.board[2][2]:
                self.winning_line = (20, 20, WIDTH - 20, cell_span * BOARD_ROWS - 20)
                return center
            # anti diagonal
            if self.board[0][2] == center == self.board[2][0]:
                self.winning_line = (WIDTH - 20, 20, 20, cell_span * BOARD_ROWS - 20)
                return center
        return None

    def is_board_full(self) -> bool:
        """Return True if no empty cells remain."""
        return all(all(cell is not None for cell in row) for row in self.board)

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """List coordinates of free cells for AI search / UI hints."""
        return [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if self.board[r][c] is None]


class Statistics:
    """Lightweight aggregate performance tracking across rounds."""

    def __init__(self) -> None:
        self.player_wins: int = 0
        self.ai_wins: int = 0
        self.draws: int = 0
        self.total_games: int = 0
        self.win_streak: int = 0
        self.best_streak: int = 0
        self.total_time_played: float = 0.0

    def record_win(self, winner: Optional[str]) -> None:
        """Update counters after a finished round."""
        self.total_games += 1
        if winner == "X":
            self.player_wins += 1
            self.win_streak += 1
            if self.win_streak > self.best_streak:
                self.best_streak = self.win_streak
        elif winner == "O":
            self.ai_wins += 1
            self.win_streak = 0
        else:
            self.draws += 1

    def reset(self) -> None:
        """Clear all accumulated statistics."""
        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0
        self.total_games = 0
        self.win_streak = 0
        self.best_streak = 0
        self.total_time_played = 0.0
