# Connect 4 Bot

Connect 4 is a two player board game, in which the players choose a color and then take turns 
dropping colores discs into a 6x7 grid. The objective of the game is to be the first to form a 
horizontal, vertical or diagonal line of four of one's own discs.

Winning Examples:

<img src="https://raw.githubusercontent.com/CrisLeaf/connect-4-bot/master/images/win1.png" height=200, width=200>
<img src="https://raw.githubusercontent.com/CrisLeaf/connect-4-bot/master/images/win2.png" height=200, width=200>
<img src="https://raw.githubusercontent.com/CrisLeaf/connect-4-bot/master/images/win3.png" height=200, width=200>
<img src="https://raw.githubusercontent.com/CrisLeaf/connect-4-bot/master/images/win4.png" height=200, width=200>


## Intro

In this reposiroty, we will teach an algorithm to play the game.

## Requirements and Run

To run the game, a Python 3.9 environment is needed, with the following libraries:
1. [NumPy](https://numpy.org/doc/stable/)
2. [Pygame](https://www.pygame.org/docs/)

To install both, on terminal enter:
```
pip install -r requirements.txt
```
and to run the game:
```
python app.py
```
Note: The bot is automatically loaded into the game.

## Methodology

We applied an algorithm inspired by the Monte Carlo Tree Search. It consists in the following:

<img src="images/mcts.png" height=250, width=600>

For each iteration we developed:

### Selection

The current state of the game is selected

### Expansion

It is expanded to a next state. In our case, we expanded each selection to its third children.

### Simulation

To not have to verify every possible game (which leads into millions 
of iterations), we just selected a simulated game after the third children. And if that game 
didn't have a winner yet, we calculated the winning percentage using a classifier.

### Backpropagation

Instead of backpropagation, we take into account the mean of all simulation's win rate, to 
decide what the next move would be.


### Classifier

We train a classifier using a dataset downloaded from
[kaggle](https://www.kaggle.com/tbrewer/connect-4). Details can be found in `classifier_train.ipynb`

The classifier consists in a CatBoost algorithm. A boosting method that focuses on processing 
categorical features and boosting trees.

## Support

Give a :star: if you like it :hugs:.
