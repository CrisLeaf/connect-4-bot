import streamlit as st
import numpy as np
import random
from bot_core import GameBot


def board_init():
	st.session_state.board = np.full((6, 7), ".", dtype=str)
	st.session_state.player = "X"
	st.session_state.winner = None
	
def get_next_open_row(j):
	for i in range(5, -1, -1):
		if st.session_state.board[i, j] == ".":
			return i

def is_valid_location(i, j):
	return st.session_state.board[i, j] == "."

def computer_player(played_mat):
	bot_move = bot.get_next_move_suggested(played_mat)

	
	# availables_col = []
	# for j in range(7):
	# 	if get_next_open_row(j) != None:
	# 		availables_col.append(j)
	# col = random.choice(availables_col)
	
	
	
	drop_piece(bot_move)

def drop_piece(j):
	i = get_next_open_row(j)
	if i != None:
		st.session_state.board[i, j] = st.session_state.player
		if not winning_move(st.session_state.player):
			st.session_state.player = "O" if st.session_state.player == "X" else "X"
		else:
			st.session_state.winner = st.session_state.player
			st.session_state.player = "O" if st.session_state.player == "X" else "X"


def get_matrix():
	played_mat = np.zeros((6, 7))
	
	for i in range(6):
		for j in range(7):
			if st.session_state.board[i, j] == "X":
				played_mat[i, j] = 1
			elif st.session_state.board[i, j] == "O":
				played_mat[i, j] = -1
			else:
				played_mat[i, j] = 0

	return played_mat

def winning_move(piece):
	# Check horizontal
	for i in range(6):
		for j in range(4):
			if st.session_state.board[i, j] == piece and \
				st.session_state.board[i, j+1] == piece and \
				st.session_state.board[i, j+2] == piece and \
				st.session_state.board[i, j+3] == piece:
				return True
	
	# Check vertical
	for i in range(3):
		for j in range(7):
			if st.session_state.board[i, j] == piece and \
				st.session_state.board[i+1, j] == piece and \
				st.session_state.board[i+2, j] == piece and \
				st.session_state.board[i+3, j] == piece:
				return True
			
	# Check positive slope diagonal
	for i in range(3):
		for j in range(3, 7):
			if st.session_state.board[i, j] == piece and \
				st.session_state.board[i+1, j-1] == piece and \
				st.session_state.board[i+2, j-2] == piece and \
				st.session_state.board[i+3, j-3] == piece:
				return True
	
	# Check negative slope diagonal
	for i in range(3):
		for j in range(4):
			if st.session_state.board[i, j] == piece and \
				st.session_state.board[i+1, j+1] == piece and \
				st.session_state.board[i+2, j+2] == piece and \
				st.session_state.board[i+3, j+3] == piece:
				return True
	

				
def main():
	st.write(
		"""
		# Connect 4 Game
		"""
	)
	
	if "board" not in st.session_state:
		board_init()
	
	reset, score, player, settings = st.columns([0.5, 0.6, 1, 1])
	reset.button("New Game", on_click=board_init)
	
	with open("style.css") as f:
		st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
		
	played_mat = get_matrix()
	
	for i, row in enumerate(st.session_state.board):
		cols = st.columns([5, 1, 1, 1, 1, 1, 1, 1, 5])
		for j, position in enumerate(row):
			cols[j+1].button(
				position,
				key=f"{i}-{j}",
				on_click=drop_piece if st.session_state.player == "X"
						 else computer_player(played_mat),
				args=(j, )
			)
	
	if st.session_state.winner:
		st.write(f"{st.session_state.winner} wins!")
		board_init()


if __name__ == "__main__":
	bot = GameBot()
	bot.load_next_moves_classifier()
	
	main()