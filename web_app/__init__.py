from flask import Flask


def create_app():
	app = Flask(__name__)
	
	from . import bot_app
	
	app.register_blueprint(bot_app.bp)
	
	return app
