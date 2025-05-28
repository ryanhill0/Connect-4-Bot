import math
import sys
import random
import numpy as np
import pygame


BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7
#difficulty values
EASY = 1
MEDIUM = 2
HARD = 3
#player 1 and 2 values

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

difficulty_1 = int(input("Select Player 1 difficulty: 1 - Easy, 2 - Medium, 3 - Hard: "))
difficulty_2 = int(input("Select Player 2 difficulty: 1 - Easy, 2 - Medium, 3 - Hard: "))

#takes input for difficulty
def difficulty_menu(difficulty_1,difficulty_2):
	# difficulty1 = difficulty_1
	# difficulty2 = difficulty_2
	if difficulty_1 == EASY:
		print("You have chosen player 1 to be Easy difficulty")
	if difficulty_1 == MEDIUM:
		print("You have chosen player 1 to be Medium difficulty")
	if difficulty_1 == HARD:
		print("You have chosen player 1 to be Hard difficulty")

	if difficulty_2== EASY:
		print("You have chosen player 2 to be Easy difficulty")
	if difficulty_2 == MEDIUM:
		print("You have chosen player 2 to be Medium difficulty")
	if difficulty_2 == HARD:
		print("You have chosen player 2 to be Hard difficulty")


def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0
def get_valid_locations(board):
	valid_locations = []
	for c in range (COLUMN_COUNT):
		if is_valid_location(board,c):
			valid_locations.append(c)
	return valid_locations

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True


def window_score(board, piece, heuristic):
	total = 0

	#centerpieces
	center_array = [int(i) for i in list(board[:,COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	total += center_count*10
	# horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r, :])]
		for c in range(COLUMN_COUNT - 3):
			window = row_array[c:c + 4]
			total+=heuristic(window,piece)
	# vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:, c])]
		for r in range(ROW_COUNT - 3):
			window = col_array[r:r + 4]
			total += heuristic(window, piece)
	# diagnal
	for r in range(3,ROW_COUNT):
		for c in range(COLUMN_COUNT - 3):
			window = [board[r - i][c + i] for i in range(4)]
			total += heuristic(window, piece)
	for r in range(3,ROW_COUNT):
		for c in range(COLUMN_COUNT - 3):
			window = [board[r - i][c - i] for i in range(4)]
			total+=heuristic(window,piece)

	return total
def medHeuristic(window, piece):
	total = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece == AI_PIECE

	if window.count(piece) == 4:
		total += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		total += 10
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		total += 5
	elif window.count(opp_piece) ==3 and window.count(EMPTY) == 1:
		total -= 8
	return total
def hardHeuristic(window, piece):
	total = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece == AI_PIECE

	if window.count(piece) == 4:
		total += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		total += 10
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		total += 5
	elif window.count(opp_piece) ==3 and window.count(EMPTY) == 1:
		total -= 80
	return total
#def pickBestMove(board,piece, heuristic):
	valid_locations = get_valid_locations(board)
	best_score = -1000
	best_col = random.choice(valid_locations)

	for c in valid_locations:
		row = get_next_open_row(board,c)
		temp_board = board.copy()
		drop_piece(temp_board,row,c,piece)
		score = window_score(temp_board,piece,heuristic)
		if score > best_score:
			best_score = score
			best_col = c
	return best_col


def terminalNode(board):
	return winning_move(board, PLAYER_PIECE) or len(get_valid_locations(board)) ==0 or winning_move(board,AI_PIECE)

def minimax(board,depth,maxplayer,heuristic):
	valid_locations = get_valid_locations(board)
	isTerminal = terminalNode(board)
	if depth ==0 or isTerminal:
		if isTerminal:
			if winning_move(board, AI_PIECE):
				return None, 1000
			elif winning_move(board, PLAYER_PIECE):
				return None, -1000
			else:
				return None, 0
		else:
			return None, window_score(board, AI_PIECE,heuristic)
	if maxplayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board,col)
			temp_board = board.copy()
			drop_piece(temp_board,row,col,AI_PIECE)
			new_score = minimax(temp_board,depth-1, False, heuristic)[1]
			if new_score > value:
				value = new_score
				column = col
		return column, value
	else:
		value = math.inf
		for col in valid_locations:
			row = get_next_open_row(board,col)
			temp_board = board.copy()
			drop_piece(temp_board,row,col,PLAYER_PIECE)
			new_score = minimax(temp_board, depth - 1,True, heuristic)[1]
			if new_score < value:
				value = new_score
				column = col
		return column,value

def abminimax(board,depth,alpha,beta,maxplayer,heuristic):
	valid_locations = get_valid_locations(board)
	isTerminal = terminalNode(board)
	if depth ==0 or isTerminal:
		if isTerminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000)
			else:
				return None, 0
		else:
			return None, window_score(board, AI_PIECE,heuristic)
	if maxplayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board,col)
			temp_board = board.copy()
			drop_piece(temp_board,row,col,AI_PIECE)
			new_score = abminimax(temp_board,depth-1,alpha, beta, False, heuristic)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value
	else:
		value = math.inf
		for col in valid_locations:
			row = get_next_open_row(board,col)
			temp_board = board.copy()
			drop_piece(temp_board,row,col,PLAYER_PIECE)
			new_score = abminimax(temp_board, depth - 1,alpha,beta,True, heuristic)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column,value


def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

#sets difficulties into a tuple
difficulty_menu(difficulty_1,difficulty_2)
diff_tup = (difficulty_1,difficulty_2)

board = create_board()

print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER,AI)
while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			# else: 
			# 	pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)

					if winning_move(board, 1):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2
					print_board(board)
					draw_board(board)


	# # Ask for Player 2 Input
	if turn == AI and not game_over:
		if diff_tup[1] == EASY:
			#Easy difficulty utilizes random piece placement
			col = random.randint(0, COLUMN_COUNT - 1)
			if is_valid_location(board, col):
				pygame.time.wait(500)
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, 2)

				if winning_move(board, 2):
					label = myfont.render("Player 2 wins!!", 1, YELLOW)
					screen.blit(label, (40,10))
					game_over = True
				print_board(board)
				draw_board(board)

				turn += 1
				turn = turn % 2


		if diff_tup[1] == MEDIUM:
			#implementing medium minmax with heuristic
			col, minimax_score = minimax(board,3, True, medHeuristic)

			if is_valid_location(board, col):
				pygame.time.wait(500)
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, 2)

				if winning_move(board, 2):
					label = myfont.render("Player 2 wins!!", 1, YELLOW)
					screen.blit(label, (40, 10))
					game_over = True
				print_board(board)
				draw_board(board)

				turn += 1
				turn = turn % 2

		if diff_tup[1] == HARD:
            #implementing medium minmax with heuristic
			col, minimax_score = abminimax(board,5,-math.inf, math.inf, True, hardHeuristic)

			if is_valid_location(board, col):
				pygame.time.wait(500)
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, 2)

				if winning_move(board, 2):
					label = myfont.render("Player 2 wins!!", 1, YELLOW)
					screen.blit(label, (40, 10))
					game_over = True
				print_board(board)
				draw_board(board)

				turn += 1
				turn = turn % 2
					


	if game_over:
		pygame.time.wait(3000)