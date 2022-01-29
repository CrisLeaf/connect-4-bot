import pickle
import numpy as np
from game_core import ROWS_COUNT, COLUMNS_COUNT, winning_move


class GameBot():
	
	def __init__(self, rows_count=ROWS_COUNT, columns_count=COLUMNS_COUNT, steps=1):
		self.rows_count = rows_count
		self.columns_count = columns_count
		self.steps = steps
	
	def load_next_moves_classifier(self):
		with open("classifier.pkl", "rb") as file:
			self.classifier = pickle.load(file)
		
		return self
	
	def get_win_probability_prediction(self, played_mat):
		"""
		Calculate the win probability of an specific game state using the classifier.
		"""
		if winning_move(played_mat, 1):
			prediction = [[-10]]
		else:
			prediction = self.classifier.predict_proba(played_mat.reshape(1, -1))
		
		return prediction[0][0]
	
	def get_column_available_position(self, played_mat, column):
		"""
		Get the available position of an specific column in an specific game state.
		"""
		try:
			available_position = np.where(played_mat[:, column] != 0)[0][0] - 1
		except:
			available_position = self.rows_count - 1
		
		return available_position
	
	def get_next_possible_moves(self, played_mat, piece, first_iteration=False):
		"""
		Get a list of all the next possible moves based on the actual game state.
		
		Params
		------
		- played_mat, numpy array : the actual game state
		- piece, {-1, 1} : the player's turn
		- first_iteration, bool : used to check move availability. If not, the function will return
								  an 'Invalid Move' element inside the list
		
		Returns
		-------
		- possible_plays_list, list : a list containing 7 lists, each one containing the next move
									  along with its children if its the case.
		"""
		possible_plays_list = []
		
		for j in range(self.columns_count):
			played_mat_copy = played_mat.copy()
			
			available_position = self.get_column_available_position(played_mat, column=j)
			
			if available_position >= 0:
				played_mat_copy[available_position, j] = piece
				possible_plays_list.append(played_mat_copy)
			elif first_iteration:
				possible_plays_list.append("Invalid Move")
				
		return possible_plays_list
	
	def get_next_move_suggested(self, played_mat):
		"""
		Get the move to play, based on win probabilities of each possible next move.

		Params
		------
		- played_mat, numpy array : the previous played matrix on which the next move
									corresponds to the bot.

		Returns
		-------
		- next_move, int : the next move column index that the bot should play.
		"""
		# Get Next Moves
		next_moves_list = self.get_next_possible_moves(played_mat, -1, first_iteration=True)
		
		# Second Moves
		second_moves_list = []
		
		for move in next_moves_list:
			if type(move) == str:
				second_moves_list.append("Invalid Move")
			else:
				next_moves = self.get_next_possible_moves(move, 1)
				next_moves.append(move)
				second_moves_list.append(next_moves)
			
		# Third Moves
		third_moves_list = []
		
		for moves_list in second_moves_list:
			if type(moves_list) == str:
				third_moves_list.append("Invalid Move")
				continue
				
			sub_list = []
			
			for index, move in enumerate(moves_list):
				next_moves = self.get_next_possible_moves(move, -1)
				
				for next_move in next_moves:
					sub_list.append(next_move)
				
				if index == len(moves_list) - 1:
					sub_list.append(move)
			
			third_moves_list.append(sub_list)
		
		# Get Probabilities
		probabilities = []
		
		for moves_list in third_moves_list:
			if type(moves_list) == str:
				probabilities.append(-100)
				continue
				
			sub_probas = []
			
			for move in moves_list:
				pred_proba = self.get_win_probability_prediction(move)
				pred_proba += np.random.uniform(-0.3, 0.3, 1)[0]
				sub_probas.append(pred_proba)
			
			probabilities.append(np.mean(sub_probas))
		
		print(probabilities)
		print(len(probabilities))
		print("\n")
		next_move = probabilities.index(max(probabilities))
		
		return next_move