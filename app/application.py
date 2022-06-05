from flask import Blueprint, request, jsonify
from .game_bot import GameBot


bp = Blueprint("application", __name__, url_prefix="/")

@bp.route("/", methods=["GET"])
def home():
    return """Home"""

@bp.route("/next", methods=["GET"])
def get_next_move():
    board = request.args.get("board")

    game_bot = GameBot()

    next_move = int(game_bot.get_next_move(board))

    return jsonify({"next-move": next_move})
