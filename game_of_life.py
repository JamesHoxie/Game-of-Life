import pygame
import random
import math
from resources import Palette as colors

pygame.init()
pygame.key.set_repeat(10, 100)

DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 600
GRID_THICKNESS = 2
BLOCK_SIZE = 12
FPS = 5

FONT = pygame.font.Font('freesansbold.ttf', 32)
game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()


# functions
def draw_grid():
	# Horizontal Lines
	for y in range(0, DISPLAY_HEIGHT, BLOCK_SIZE):
		pygame.draw.line(game_display, colors.BLACK, (0, y), (DISPLAY_WIDTH, y), GRID_THICKNESS)

	# Vertical Lines
	for x in range(0, DISPLAY_WIDTH, BLOCK_SIZE):
		pygame.draw.line(game_display, colors.BLACK, (x, 0), (x, DISPLAY_HEIGHT), GRID_THICKNESS)

# draws all currently living cells to grid
def draw_cells(living_cells):
	for cell in living_cells:
		cell_x, cell_y = cell[0], cell[1]
		pygame.draw.rect(game_display, colors.GREEN, (cell_x, cell_y, BLOCK_SIZE, BLOCK_SIZE))


def update_cells(living_cells):
	# list of relevant dead cells that may come back to life this step if 3 living cells neighbor any of them
	neighboring_dead_cells = {}
	cells_to_remove = []

	for cell in living_cells:
		cell_x, cell_y = cell[0], cell[1]

		num_neighbors, neighboring_dead_cells = check_neighbors(cell, living_cells, neighboring_dead_cells)

		if num_neighbors == 2 or num_neighbors == 3:
			# cell keeps living this step
			continue

		else:
			# cell dies this step
			cells_to_remove.append(cell)

	# remove all cells that will die this step from living cells
	for cell in cells_to_remove:
		del living_cells[cell]

	# bring any cells to life with exactly 3 neighbors
	for dead_cell in neighboring_dead_cells:
		if neighboring_dead_cells[dead_cell] == 3:
			living_cells[dead_cell] = 1

	return living_cells


# check neighboring cells in 8 directions for number of living cells and return, as well as update list of neighboring_dead_cells to living cells
def check_neighbors(cell, living_cells, neighboring_dead_cells):
	def get_neighbors(cell):
		cell_x, cell_y = cell[0], cell[1]

		return [(cell_x - BLOCK_SIZE, cell_y), 
				(cell_x - BLOCK_SIZE, cell_y - BLOCK_SIZE),
				(cell_x, cell_y - BLOCK_SIZE),
				(cell_x + BLOCK_SIZE, cell_y - BLOCK_SIZE), 
				(cell_x + BLOCK_SIZE, cell_y),
				(cell_x + BLOCK_SIZE, cell_y + BLOCK_SIZE),
				(cell_x, cell_y + BLOCK_SIZE), 
				(cell_x - BLOCK_SIZE, cell_y + BLOCK_SIZE)]

	# returns 1 if this neighbor cell is living, 0 otherwise
	def process_neighbor(neighbor_cell):
		if neighbor_cell in living_cells:
			return 1
		
		else:
			if neighbor_cell in neighboring_dead_cells:
				neighboring_dead_cells[neighbor_cell] += 1
			else: 
				neighboring_dead_cells[neighbor_cell] = 1

		return 0

	num_living_neighbors = 0

	for neighbor_cell in get_neighbors(cell):
		num_living_neighbors += process_neighbor(neighbor_cell)

	
	return num_living_neighbors, neighboring_dead_cells


def pause():
	PAUSE_FONT = pygame.font.Font("freesansbold.ttf", 35)
	pause_text = PAUSE_FONT.render("Paused", True, colors.WHITE, colors.BLACK)
	pause_rect = pause_text.get_rect()
	pause_rect.center = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)
	paused = True

	game_display.blit(pause_text, pause_rect)
	pygame.display.update()

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					return True

		clock.tick(5)

def game_loop(start_cells):
	running = True
	game_over = False
	dt = 0
	living_cells = start_cells

	while running:
		if game_over:
			game_over_text = FONT.render("Game Over", True, colors.WHITE, colors.BLACK)
			game_over_rect = game_over_text.get_rect()
			game_over_rect.x = DISPLAY_WIDTH / 2 - (game_over_rect.right - game_over_rect.left) / 2
			game_over_rect.y = DISPLAY_HEIGHT / 2
			game_display.blit(game_over_text, game_over_rect)
			pygame.display.update()

		while game_over:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					game_over = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						running = False
						game_over = False
						
		#Process input (events)
		for event in pygame.event.get():
			#check for closing window
			if event.type == pygame.QUIT:
				running = False

			# check for player input
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					running = pause()

		#Update
		living_cells = update_cells(living_cells)

		#Draw/Render
		game_display.fill(colors.WHITE)
		draw_cells(living_cells)
		draw_grid()

		pygame.display.update()
		# use dt to speed up tetrimino blocks later
		dt += clock.tick(FPS)


# block
# start_cells = {(50, 50): 1, (62, 50): 1, (50, 62): 1, (62, 62): 1}

# blinker
# start_cells = {(50, 50): 1, (62, 50): 1, (74, 50): 1}

# TODO: Test this with random starting cells
game_loop(start_cells)
pygame.quit()