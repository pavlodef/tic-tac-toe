"""Rendering layer: pygame drawing and UI composition.

Pure rendering functions; game state is read-only here.
"""

from typing import Optional, Tuple
import pygame
import math
from constants import (
    WIDTH, HEIGHT, LINE_WIDTH, BOARD_ROWS, BOARD_COLS, CELL_SIZE,
    CIRCLE_RADIUS, CIRCLE_WIDTH, CROSS_WIDTH, SPACE,
    BG_COLOR, LINE_COLOR, CROSS_COLOR, CIRCLE_COLOR,
    RED, BUTTON_COLOR, BUTTON_HOVER, MENU_BG, MENU_BUTTON,
    MENU_BUTTON_HOVER, TEXT_COLOR, STATS_BG, GOLD, SILVER,
    DIFFICULTY_COLORS, BOARD_PIXEL_HEIGHT
)


class Renderer:
    """Handles drawing of board, figures, HUD, animations, and menus."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_large = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 32)
        self.font_small = pygame.font.SysFont("Arial", 24)
        self.font_tiny = pygame.font.SysFont("Arial", 18)
        self.restart_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 80, 140, 50)
        self.menu_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 80, 130, 50)
        self.animation_progress = 0
        self.win_animation_frame = 0

    def get_button_rect(self) -> pygame.Rect:
        return self.restart_button
    
    def get_menu_button_rect(self) -> pygame.Rect:
        return self.menu_button

    def draw_board(self) -> None:
        """Draw background and board grid lines."""
        self.screen.fill(BG_COLOR)
        
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(
                self.screen, LINE_COLOR,
                (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE),
                LINE_WIDTH
            )
        
        for i in range(1, BOARD_COLS):
            pygame.draw.line(
                self.screen, LINE_COLOR,
                (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_PIXEL_HEIGHT),
                LINE_WIDTH
            )

    def draw_figures(self, game_state, animate: bool = False) -> None:
        """Render X and O marks with optional animation."""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if game_state.board[row][col] == "O":
                    center_x = int(col * CELL_SIZE + CELL_SIZE / 2)
                    center_y = int(row * CELL_SIZE + CELL_SIZE / 2)
                    
                    if animate and self.animation_progress < 1.0:
                        radius = int(CIRCLE_RADIUS * self.animation_progress)
                    else:
                        radius = CIRCLE_RADIUS
                    
                    pygame.draw.circle(
                        self.screen,
                        CIRCLE_COLOR,
                        (center_x, center_y),
                        radius,
                        CIRCLE_WIDTH,
                    )
                elif game_state.board[row][col] == "X":
                    start_desc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE)
                    end_desc = ((col + 1) * CELL_SIZE - SPACE, (row + 1) * CELL_SIZE - SPACE)
                    
                    start_asc = (col * CELL_SIZE + SPACE, (row + 1) * CELL_SIZE - SPACE)
                    end_asc = ((col + 1) * CELL_SIZE - SPACE, row * CELL_SIZE + SPACE)
                    
                    if animate and self.animation_progress < 1.0:
                        mid_desc_x = start_desc[0] + (end_desc[0] - start_desc[0]) * self.animation_progress
                        mid_desc_y = start_desc[1] + (end_desc[1] - start_desc[1]) * self.animation_progress
                        mid_asc_x = start_asc[0] + (end_asc[0] - start_asc[0]) * self.animation_progress
                        mid_asc_y = start_asc[1] + (end_asc[1] - start_asc[1]) * self.animation_progress
                        
                        pygame.draw.line(self.screen, CROSS_COLOR, start_desc, (mid_desc_x, mid_desc_y), CROSS_WIDTH)
                        pygame.draw.line(self.screen, CROSS_COLOR, start_asc, (mid_asc_x, mid_asc_y), CROSS_WIDTH)
                    else:
                        pygame.draw.line(self.screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                        pygame.draw.line(self.screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

    def draw_winning_line(self, game_state) -> None:
        if game_state.winning_line:
            self.win_animation_frame += 1
            alpha = abs(math.sin(self.win_animation_frame * 0.1)) * 255
            
            line_surface = pygame.Surface((WIDTH, BOARD_PIXEL_HEIGHT), pygame.SRCALPHA)
            color_with_alpha = (*RED, int(alpha))
            
            pygame.draw.line(
                line_surface, color_with_alpha,
                (game_state.winning_line[0], game_state.winning_line[1]),
                (game_state.winning_line[2], game_state.winning_line[3]),
                12
            )
            self.screen.blit(line_surface, (0, 0))

    def draw_button(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        
        restart_color = BUTTON_HOVER if self.restart_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, restart_color, self.restart_button, border_radius=10)
        restart_text = self.font_small.render("Restart", True, TEXT_COLOR)
        restart_rect = restart_text.get_rect(center=self.restart_button.center)
        self.screen.blit(restart_text, restart_rect)
        
        menu_color = MENU_BUTTON_HOVER if self.menu_button.collidepoint(mouse_pos) else MENU_BUTTON
        pygame.draw.rect(self.screen, menu_color, self.menu_button, border_radius=10)
        menu_text = self.font_small.render("Menu", True, TEXT_COLOR)
        menu_rect = menu_text.get_rect(center=self.menu_button.center)
        self.screen.blit(menu_text, menu_rect)

    def draw_turn_indicator(self, game_state) -> None:
        if not game_state.game_over:
            indicator_text = "Your Turn (X)" if game_state.player == "X" else "AI Thinking..."
            color = CROSS_COLOR if game_state.player == "X" else CIRCLE_COLOR
            
            text = self.font_tiny.render(indicator_text, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            self.screen.blit(text, text_rect)
    
    def draw_game_result(self, game_state) -> None:
        """Overlay end-of-game result banner with subtle background."""
        if game_state.game_over:
            if game_state.winner == "X":
                message = "You Win! 🎉"
                color = GOLD
            elif game_state.winner == "O":
                message = "AI Wins!"
                color = RED
            else:
                message = "Draw!"
                color = SILVER
            
            text = self.font_medium.render(message, True, color)
            bg_rect = pygame.Rect(WIDTH // 2 - 120, BOARD_PIXEL_HEIGHT // 2 - 30, 240, 60)
            
            s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 0, 0, 180), s.get_rect(), border_radius=15)
            self.screen.blit(s, bg_rect.topleft)
            
            text_rect = text.get_rect(center=bg_rect.center)
            self.screen.blit(text, text_rect)
    
    def draw_stats(self, stats, difficulty: str) -> None:
        """Draw difficulty and compact stats under the board."""
        stats_y = BOARD_PIXEL_HEIGHT + 15
        
        diff_text = self.font_small.render(f"Difficulty: {difficulty}", True, DIFFICULTY_COLORS.get(difficulty, TEXT_COLOR))
        self.screen.blit(diff_text, (10, stats_y))
        
        win_rate = (stats.player_wins / stats.total_games * 100) if stats.total_games > 0 else 0
        
        stats_parts = [
            f"W: {stats.player_wins}",
            f"L: {stats.ai_wins}",
            f"D: {stats.draws}",
            f"Rate: {win_rate:.0f}%"
        ]
        
        if stats.win_streak > 0:
            stats_parts.append(f"🔥{stats.win_streak}")
        if stats.best_streak > 0:
            stats_parts.append(f"⭐{stats.best_streak}")
        
        stats_text = self.font_tiny.render(" | ".join(stats_parts), True, TEXT_COLOR)
        self.screen.blit(stats_text, (10, stats_y + 30))
    
    def render(self, game_state, stats=None, difficulty="Hard") -> None:
        self.draw_board()
        self.draw_figures(game_state)
        self.draw_button()
        if stats:
            self.draw_stats(stats, difficulty)
        self.draw_turn_indicator(game_state)
        self.draw_winning_line(game_state)
        self.draw_game_result(game_state)
        pygame.display.update()
        
        if self.animation_progress < 1.0:
            self.animation_progress += 0.15
    
    def reset_animation(self) -> None:
        """Reset simple animation counters."""
        self.animation_progress = 0
        self.win_animation_frame = 0

    def get_clicked_cell(self, pos: Tuple[int, int]) -> Tuple[Optional[int], Optional[int]]:
        """Translate mouse coords into (row, col) if inside the grid."""
        mouse_x, mouse_y = pos
        if mouse_y < BOARD_PIXEL_HEIGHT:
            clicked_row = mouse_y // CELL_SIZE
            clicked_col = mouse_x // CELL_SIZE
            return clicked_row, clicked_col
        return None, None
    
    def draw_menu(self) -> list:
        """Render difficulty selection menu and return clickable rects."""
        self.screen.fill(MENU_BG)
        
        title = self.font_large.render("TIC-TAC-TOE", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_small.render("Choose Difficulty", True, SILVER)
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 160))
        self.screen.blit(subtitle, subtitle_rect)
        
        difficulties = ["Easy", "Medium", "Hard", "Impossible"]
        buttons = []
        
        for i, diff in enumerate(difficulties):
            button_y = 220 + i * 90
            button_rect = pygame.Rect(WIDTH // 2 - 150, button_y, 300, 60)
            buttons.append((button_rect, diff))
            
            mouse_pos = pygame.mouse.get_pos()
            is_hover = button_rect.collidepoint(mouse_pos)
            color = MENU_BUTTON_HOVER if is_hover else MENU_BUTTON
            
            pygame.draw.rect(self.screen, color, button_rect, border_radius=15)
            pygame.draw.rect(self.screen, DIFFICULTY_COLORS[diff], button_rect, 3 if is_hover else 2, border_radius=15)
            
            text = self.font_medium.render(diff, True, TEXT_COLOR)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
        
        hint_text = self.font_tiny.render("Shortcuts: R - Restart | M/ESC - Menu", True, SILVER)
        hint_rect = hint_text.get_rect(center=(WIDTH // 2, HEIGHT - 25))
        self.screen.blit(hint_text, hint_rect)
        
        pygame.display.update()
        return buttons
