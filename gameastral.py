import pygame
import random
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Conway\'s Game of Life')

# Define fonts
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

# Utility functions
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    draw_text(text, font, WHITE, screen, x + width / 2, y + height / 2)

def draw_slider(label, x, y, value, min_val, max_val, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    slider_width = 300
    handle_radius = 10
    slider_height = 4

    # Draw the slider line
    pygame.draw.rect(screen, DARK_GRAY, (x, y, slider_width, slider_height))

    # Calculate the handle position
    handle_x = x + int((value - min_val) / (max_val - min_val) * slider_width)
    handle_y = y + slider_height // 2

    # Draw the handle
    pygame.draw.circle(screen, BLUE, (handle_x, handle_y), handle_radius)

    # Check if the handle is being dragged
    if click[0] == 1 and handle_x - handle_radius < mouse[0] < handle_x + handle_radius and handle_y - handle_radius < mouse[1] < handle_y + handle_radius:
        new_value = min_val + (mouse[0] - x) / slider_width * (max_val - min_val)
        if action:
            action(new_value)

    # Draw the label and current value
    draw_text(f'{label}: {int(value) if isinstance(value, int) else round(value, 1)}', small_font, BLACK, screen, x + slider_width / 2, y - 20)

# Parameters
grid_size = 50
cycles = 1000
update_time = 0.5

# Function to change grid size
def set_grid_size(value):
    global grid_size
    grid_size = int(value)

# Function to change cycles
def set_cycles(value):
    global cycles
    cycles = int(value)

# Function to change update time
def set_update_time(value):
    global update_time
    update_time = round(value, 1)

# Main menu
def main_menu():
    running = True
    while running:
        screen.fill(WHITE)

        draw_text('Conway\'s Game of Life', font, BLACK, screen, WIDTH / 2, HEIGHT / 4)

        draw_button('Start', WIDTH / 2 - 100, HEIGHT / 2 - 50, 200, 50, GRAY, DARK_GRAY, start_game)
        draw_button('Parameters', WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 50, GRAY, DARK_GRAY, parameters_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Parameters menu
def parameters_menu():
    running = True
    while running:
        screen.fill(WHITE)

        draw_text('Parameters', font, BLACK, screen, WIDTH / 2, HEIGHT / 8)

        draw_slider('Grid Size', WIDTH / 2 - 150, HEIGHT / 4, grid_size, 30, 100, set_grid_size)
        draw_slider('Cycles', WIDTH / 2 - 150, HEIGHT / 4 + 100, cycles, 1, 10000, set_cycles)
        draw_slider('Update Time', WIDTH / 2 - 150, HEIGHT / 4 + 200, update_time, 0.1, 5.0, set_update_time)

        draw_button('Save', WIDTH / 2 - 100, HEIGHT / 2 + 150, 200, 50, GRAY, DARK_GRAY, main_menu)
        draw_button('Reset', WIDTH / 2 - 100, HEIGHT / 2 + 230, 200, 50, GRAY, DARK_GRAY, reset_parameters)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Reset parameters to default values
def reset_parameters():
    global grid_size, cycles, update_time
    grid_size = 50
    cycles = 1000
    update_time = 0.5

# Game of Life logic
class Node:
    def __init__(self, xy):
        self.xy = xy
        self.on = False
        self.next = False

    def set_next_state(self, on):
        self.next = on

    def update(self):
        self.on = self.next

def gen_nodes(rows, cols):
    return [[Node((x, y)) for y in range(cols)] for x in range(rows)]

def get_neighbors(grid):
    rows, cols = len(grid), len(grid[0])
    for x in range(rows):
        for y in range(cols):
            neighbors = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols:
                        neighbors.append(grid[nx][ny])
            grid[x][y].neighbors = neighbors

def rule_check(grid):
    for row in grid:
        for node in row:
            live_neighbors = sum(neighbor.on for neighbor in node.neighbors)
            if node.on:
                if live_neighbors < 2 or live_neighbors > 3:
                    node.set_next_state(False)
                else:
                    node.set_next_state(True)
            else:
                if live_neighbors == 3:
                    node.set_next_state(True)

def scatter(grid, chance=0.2):
    for row in grid:
        for node in row:
            if random.random() < chance:
                node.on = True

def live(grid, limit, screen, cell_size, update_time):
    rows, cols = len(grid), len(grid[0])
    clock = pygame.time.Clock()
    current_update_time = update_time
    for _ in range(limit):
        rule_check(grid)
        for row in grid:
            for node in row:
                node.update()
        draw_grid(screen, grid, cell_size)
        draw_text(f'Update Time: {current_update_time}', small_font, BLACK, screen, WIDTH / 2, HEIGHT - 50)
        pygame.display.flip()
        clock.tick(1 / current_update_time)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                    current_update_time *= 0.9
                elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
                    current_update_time *= 1.1
                current_update_time = max(0.1, min(current_update_time, 5.0))

def draw_grid(screen, grid, cell_size):
    screen.fill(WHITE)
    for row in grid:
        for node in row:
            color = (0, 0, 0) if node.on else (255, 255, 255)
            rect = pygame.Rect(node.xy[1] * cell_size, node.xy[0] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect)
