import pickle
import numpy as np
import random
from .game_core import ROWS_COUNT, COLUMNS_COUNT, winning_move
from catboost import CatBoostClassifier
import time


class GameBot():
	
	def __init__(self, rows_count=ROWS_COUNT, columns_count=COLUMNS_COUNT,
				 steps=1, bot_difficulty=1):
		self.rows_count = rows_count
		self.columns_count = columns_count
		self.steps = steps
		self.bot_difficulty = bot_difficulty
	
	def load_classifier(self):
		with open("web_app/static/classifier.pkl", "rb") as file:
			self.classifier = pickle.load(file)
		
		return self
	
	def _get_win_probability_prediction(self, played_mat):
		"""
		Calculate the win probability of an specific state using the classifier.
		"""
		if winning_move(played_mat, 1):
			prediction = [[-0.4 * (self.bot_difficulty ** 4)]]
		elif winning_move(played_mat, -1):
			prediction = [[0.4 * (self.bot_difficulty ** 3)]]
		else:
			prediction = self.classifier.predict_proba(played_mat.reshape(1, -1))
		
		return prediction[0][0]
	
	def _get_column_available_position(self, played_mat, column):
		"""
		Get the available position of an specific column in an specific delete state.
		"""
		try:
			available_position = np.where(played_mat[:, column] != 0)[0][0] - 1
		except:
			available_position = self.rows_count - 1
		
		return available_position
	
	def _get_next_possible_moves(self, played_mat, piece, first_iteration=False):
		"""
		Get a list of all the next possible moves based on the actual delete state.
		
		Params
		------
		- played_mat, numpy array : the actual delete state,
		- piece, {-1, 1} : the player's turn,
		- first_iteration, bool : used to check move availability. If not, the function will return
								  an 'Invalid Move' element inside the list.
		
		Returns
		-------
		- possible_plays_list, list : a list containing 7 lists, each one containing the next move
									  along with its children if its the case.
		"""
		possible_plays_list = []
		
		for j in range(self.columns_count):
			played_mat_copy = played_mat.copy()
			
			available_position = self._get_column_available_position(played_mat, column=j)
			
			if available_position >= 0:
				played_mat_copy[available_position, j] = piece
				possible_plays_list.append(played_mat_copy)
			elif first_iteration:
				possible_plays_list.append("Invalid Move")
		
		return possible_plays_list
	
	def _get_available_columns(self, played_mat):
		"""
		Get the available columns of the current delete state.
		
		Params
		------
		- played_mat, numpy array : the actual delete state.
		
		Returns
		-------
		- available_columns, list : list of available column indexes.
		"""
		available_columns = []
		
		for col in range(self.columns_count):
			available_position = self._get_column_available_position(played_mat, col)
			
			if available_position >= 0:
				available_columns.append(col)
		
		return available_columns
	
	def _get_simulated_game(self, played_mat, next_turn, future_steps=5):
		"""
		Randomly simulate a delete of an specific number of plays.
		
		Params
		------
		- played_mat, numpy array : the actual delete state,
		- next_turn, {-1, 1} : the player's turn,
		- future_steps, int : the number of plays to be simulated.
		
		Returns
		-------
		- simulated_game, numpy array : the simulated delete matrix.
		"""
		simulated_game = played_mat.copy()
		for i in range(future_steps * self.bot_difficulty):
			available_columns = self._get_available_columns(simulated_game)
			if len(available_columns) == 0:
				break
			
			random_col = random.sample(available_columns, 1)[0]
			
			available_position = self._get_column_available_position(simulated_game,
																	 column=random_col)
			
			if available_position >= 0:
				simulated_game[available_position, random_col] = next_turn * (-1) ** i
			
			if winning_move(simulated_game, next_turn * (-1) ** i):
				break
		
		return simulated_game
	
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
		# Get Next Moves
		next_moves_list = self._get_next_possible_moves(played_mat, -1, first_iteration=True)
		
		# Second Moves
		second_moves_list = []
		
		for move in next_moves_list:
			if type(move) == str:
				second_moves_list.append("Invalid Move")
			else:
				next_moves = self._get_next_possible_moves(move, 1)
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
				next_moves = self._get_next_possible_moves(move, -1)
				
				for next_move in next_moves:
					sub_list.append(next_move)
				
				if index == len(moves_list) - 1:
					sub_list.append(move)
			
			third_moves_list.append(sub_list)
		
		# Get Simulations
		simulated_moves_list = []
		
		for moves_list in third_moves_list:
			if type(moves_list) == str:
				simulated_moves_list.append("Invalid Move")
				continue
			
			sub_list = []
			
			for move in moves_list:
				for _ in range(1 * self.bot_difficulty):
					simulated_game = self._get_simulated_game(move, next_turn=1)
					sub_list.append(simulated_game)
				sub_list.append(move)
			
			simulated_moves_list.append(sub_list)
		
		# Get Probabilities
		probabilities = []
		
		simulated_moves_count = 0
		for moves_list in simulated_moves_list:
			if type(moves_list) == str:
				probabilities.append(-100)
				continue
			
			sub_probas = []
			
			for move in moves_list:
				pred_proba = self._get_win_probability_prediction(move)
				pred_proba += np.random.uniform(
					-0.2 * ((4 - self.bot_difficulty) ** 2.5),
					0.2 * ((4 - self.bot_difficulty) ** 2.5),
					1
				)[0]
				
				sub_probas.append(pred_proba)
				
				simulated_moves_count += 1
			
			probabilities.append(np.mean(sub_probas))
		
		next_move = probabilities.index(max(probabilities))
		
		if 1250 <= simulated_moves_count < 1500:
			time.sleep(0.2)
		elif 1000 <= simulated_moves_count < 1250:
			time.sleep(0.4)
		elif 750 <= simulated_moves_count < 1000:
			time.sleep(0.8)
		elif 500 <= simulated_moves_count < 750:
			time.sleep(1)
		elif 250 <= simulated_moves_count < 500:
			time.sleep(1.3)
		elif simulated_moves_count < 250:
			time.sleep(1.5)
		
		return next_move
