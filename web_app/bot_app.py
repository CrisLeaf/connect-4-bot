from flask import Blueprint, render_template, request, jsonify
import numpy as np
from .bot_core import GameBot
import json


bp = Blueprint("web_app", __name__, url_prefix="/")

@bp.route("/")
def home_page():
	global game_bot
	game_bot = GameBot(bot_difficulty=3)
	game_bot.load_classifier()
	return render_template("connect4.html")

@bp.route("/getmethod", methods=["POST"])
def post_me():
	game_array = json.loads(request.data.decode())["game_array"]
	
	game_array = game_array.replace("]]", "")
	game_array = game_array.replace("[[", "")
	
	game_array = game_array.split("],[")
	
	game_array = [[int(element) for element in row.split(",")] for row in game_array]
	game_array = np.array(game_array)
	
	bot_move = game_bot.get_next_move(game_array)
	
	responses = {"bot_move": str(bot_move)}
	
	return jsonify(responses)
