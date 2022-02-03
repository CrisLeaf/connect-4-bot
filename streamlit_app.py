import streamlit as st
import numpy as np


def board_init(post_init=False):
	# if not post_init:
	# 	st.session_state.win = {"X": 0, "O": 0}

	# st.session_state.board = np.full((6, 7), ".", dtype=str)
	
	st.session_state.board = np.zeros((6, 7))
	st.session_state.player = "X"

	
def player_play(i, j):
	st.session_state.board[i, j] = 1
	
def bot_play():
	i = np.random.randint(0, 5, 1)
	j = np.random.randint(0, 6, 1)
	st.session_state.board[i, j] = -1

def main():
	st.write(
		"""
		# Connect 4
		"""
	)
	
	if "board" not in st.session_state:
		board_init()
	
	for i, row in enumerate(st.session_state.board):
		cols = st.columns([5, 1, 1, 1, 1, 1, 1, 5])
		
		for j, position in enumerate(row):
			if position > 0:
				cols[j + 1].button("O", key=f"{i}-{j}")
			elif position < 0:
				cols[j + 1].button("X", key=f"{i}-{j}")
			else:
				cols[j + 1].button(".", key=f"{i}-{j}", on_click=player_play, args=(i, j))
			
	bot_play()


if __name__ == "__main__":
	main()