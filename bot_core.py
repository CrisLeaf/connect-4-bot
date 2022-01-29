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
			
		return prediction
	
	def get_column_available_position(self, played_mat, column):
		"""
		Get the available position of an specific column in an specific game state.
		"""
		try:
			available_position = np.where(played_mat[:, column] != 0)[0][0] - 1
		except:
			available_position = self.rows_count - 1
		
		return available_position
	
	def get_next_moves_win_probabilities(self, played_mat, max_steps=3):
		"""
		Get the win probabilities of each next possible play
		
		Params
		------
		 - played_mat, numpy array: the actual state of the game.
		 - max_steps, int=3: the maximum state to look further
		 					 (Note: The calculation time grows exponentially)
		 
		Returns
		-------
		- final_probas, list: the list of the next movement winning probabilities, calculated
							  averaging the probabilities of wining for each max_step children,
							  if possible.
		"""
		global pred_probas
		final_probas = []
		
		# for j in range(self.columns_count):
		for j in range(self.columns_count):
			played_mat_copy = played_mat.copy()
			stop_loop = False

			available_position = self.get_column_available_position(played_mat_copy, column=j)
			
			if available_position >= 0:
				played_mat_copy[available_position, j] = (-1) ** self.steps
				
				print(self.steps)
				
				if self.steps < 3:
					self.steps += 1
					pred_probas = self.get_next_moves_win_probabilities(played_mat_copy)
				else:
					stop_loop = True
		
			else:
				if self.steps == 1:
					final_probas.append(-100)
					
				if j == self.columns_count - 1:
					self.steps = 1
					
				continue
		
			if stop_loop:
				pred_proba = self.get_win_probability_prediction(played_mat_copy)
				pred_proba += np.random.uniform(-0.3, 0.3, 1)
				final_probas.append(pred_proba[0][0])
				
				if j == self.columns_count - 1:
					self.steps = 1
			
			else:
				final_probas.append(np.mean(pred_probas))
			
		return final_probas
	
	def get_next_move(self, played_mat):
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
		probabilities = self.get_next_moves_win_probabilities(played_mat)
		
		if len(probabilities) < 7:
			
			for j in range(self.columns_count):
				last_position = self.get_column_available_position(played_mat, column=j)
				
				if last_position >= 0:
					return last_position
		
		next_move = probabilities.index(max(probabilities))
		
		return next_move