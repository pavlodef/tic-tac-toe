"""Application entrypoint for the Tic-Tac-Toe.

Coordinates pygame window lifecycle, difficulty selection menu, threaded AI
turns, rendering, and statistics updates. Kept intentionally lightweight so
logic remains in dedicated modules.
"""
import pygame
import sys
import random
import threading
import time

from constants import WIDTH, HEIGHT
from game_logic import GameState, Statistics
from ai import AIPlayer
from renderer import Renderer


class Game:
    """Top-level controller wiring state, AI, renderer, and event loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe")
        
        self.game_state = GameState()
        self.statistics = Statistics()
        self.renderer = Renderer(self.screen)
        self.difficulty = None
        self.ai_player = None
        self.in_menu = True
        self.clock = pygame.time.Clock()
        self.ai_thinking = False
    
    def select_difficulty(self) -> bool:
        """Render menu and process a single frame of difficulty selection.

        Returns False when user quits, True otherwise to continue loop.
        """
        buttons = self.renderer.draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, diff in buttons:
                    if button_rect.collidepoint(event.pos):
                        self.difficulty = diff
                        self.ai_player = AIPlayer(self.game_state.board, difficulty=diff)
                        self.in_menu = False
                        self.renderer.reset_animation()
                        
                        if diff in ["Hard", "Impossible"] and random.random() < 0.5:
                            self.renderer.render(self.game_state, self.statistics, self.difficulty)
                            pygame.display.update()
                            pygame.time.wait(100)
                            self.make_ai_move()
                        
                        return True
        
        return True
    
    def make_ai_move(self):
        """Spawn background thread to compute/apply AI move (non-blocking)."""
        if not self.ai_thinking and not self.game_state.game_over:
            self.ai_thinking = True
            
            def ai_move_thread():
                move = self.ai_player.get_move(self.game_state)
                
                if move:
                    self.game_state.board[move[0]][move[1]] = "O"
                    self.renderer.reset_animation()
                    self.game_state.winner = self.game_state.check_winner()
                    if self.game_state.winner or self.game_state.is_board_full():
                        self.game_state.game_over = True
                        self.statistics.record_win(self.game_state.winner)
                
                self.ai_thinking = False
            
            thread = threading.Thread(target=ai_move_thread)
            thread.daemon = True
            thread.start()
    
    def handle_game_event(self, event) -> bool:
        """Handle one pygame event in active game screen.

        Returns False to signal application exit.
        """
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game_state.reset()
                self.renderer.reset_animation()
                self.ai_thinking = False
                return True
            elif event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                self.in_menu = True
                self.game_state.reset()
                self.renderer.reset_animation()
                self.ai_thinking = False
                return True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.renderer.get_button_rect().collidepoint(event.pos):
                self.game_state.reset()
                self.renderer.reset_animation()
                self.ai_thinking = False
                return True
            
            if self.renderer.get_menu_button_rect().collidepoint(event.pos):
                self.in_menu = True
                self.game_state.reset()
                self.renderer.reset_animation()
                self.ai_thinking = False
                return True
            
            if not self.game_state.game_over and not self.ai_thinking:
                row, col = self.renderer.get_clicked_cell(event.pos)
                if row is not None and col is not None:
                    if self.game_state.make_move(row, col):
                        self.renderer.reset_animation()
                        
                        self.game_state.winner = self.game_state.check_winner()
                        if self.game_state.winner or self.game_state.is_board_full():
                            self.game_state.game_over = True
                            self.statistics.record_win(self.game_state.winner)
                        else:
                            self.make_ai_move()
        
        return True
    
    def run(self) -> None:
        """Main loop alternating between menu and in-game rendering."""
        running = True
        
        while running:
            if self.in_menu:
                running = self.select_difficulty()
            else:
                for event in pygame.event.get():
                    running = self.handle_game_event(event)
                    if not running:
                        break
                
                self.renderer.render(self.game_state, self.statistics, self.difficulty)
            
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


def main() -> None:
    """Entrypoint helper used by __main__ guard."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
