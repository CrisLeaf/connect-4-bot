import pickle

with open("classifier.pkl", "rb") as f:
	classifier = pickle.load(f)
	
#%%
import pandas as pd

df = pd.read_csv("c4_game_database.csv")
df = df.sample(frac=1)
df = df.copy()

#%%
classifier.predict(df.drop(columns="winner")[0:100])

#%%
import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
zeros_mat = np.zeros((ROW_COUNT, COLUMN_COUNT))

#%%
new_df = pd.DataFrame(data=zeros_mat.reshape(1, -1), columns=df.columns[0:42])


#%%
zeros_mat = np.zeros((ROW_COUNT, COLUMN_COUNT))

# for j in [1, 3, 4, 5]:
# 	zeros_mat[5, j] = 1
# 	zeros_mat[4, j] = 1


print(zeros_mat)

#%%
prediction_probabilities = []
for j in range(7):
	zeros_mat_ = zeros_mat.copy()

	try:
		available_index = np.where(zeros_mat[:, j] != 0)[0][0] - 1
		if available_index >= 0:
			zeros_mat_[available_index, j] = -1
		else:
			continue
	except:
		zeros_mat_[5, j] = -1
	
	print(zeros_mat_)
	prediction = classifier.predict_proba(zeros_mat_.reshape(1, -1))
	print(prediction)
	prediction_probabilities.append(prediction[0][0])
	print("\n")
	
print(prediction_probabilities)

