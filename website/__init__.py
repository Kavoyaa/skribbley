from flask import Flask
from flask_socketio import join_room, leave_room, send, SocketIO

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = '1234'
	
	from .views import views

	app.register_blueprint(views, url_prefix='/')
		
	return app

def create_socket(app):
	socketio = SocketIO(app)
	return socketio
