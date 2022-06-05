from flask import Blueprint
from .game_bot import GameBot

bp = Blueprint("application", __name__, url_prefix="/")

@bp.route("/", methods=["GET"])
def home():
    global game_bot
    game_bot = GameBot()

    return """Home"""

@bp.route("/next", methods=["GET"])
def get_next_move():
    board = request.args.get("board")
    next_move = bot.get_next_move(board)

    return jsonify({"next-move": next_move})
