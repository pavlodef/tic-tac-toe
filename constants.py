"""Game constants and configuration.

Only UI-agnostic values live here to keep rendering predictable. The board is
always a square of WIDTH x WIDTH pixels; extra vertical space is reserved for
controls and stats.
"""

WIDTH, HEIGHT = 600, 750  # window size
BOARD_ROWS, BOARD_COLS = 3, 3
CELL_SIZE = WIDTH // BOARD_COLS
BOARD_PIXEL_HEIGHT = CELL_SIZE * BOARD_ROWS  # area occupied by the grid

LINE_WIDTH = 5
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = CELL_SIZE // 4

RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CROSS_COLOR = (66, 66, 66)
CIRCLE_COLOR = (239, 231, 200)
BUTTON_COLOR = (50, 150, 50)
BUTTON_HOVER = (70, 180, 70)
MENU_BG = (44, 62, 80)
MENU_BUTTON = (52, 73, 94)
MENU_BUTTON_HOVER = (72, 93, 114)
TEXT_COLOR = (236, 240, 241)
STATS_BG = (34, 49, 63)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

DIFFICULTY_COLORS = {
    "Easy": (46, 204, 113),
    "Medium": (241, 196, 15),
    "Hard": (230, 126, 34),
    "Impossible": (231, 76, 60)
}
