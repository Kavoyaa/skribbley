from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random

views = Blueprint('views', __name__)

rooms = {}

def generate_code(length=4):
	code = ""
	for i in range(length):
		code += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
	
	if code in rooms:
		generate_code(length=length)
	else:
		return code

@views.route('/', methods=["POST", "GET"])
def home():
	session.clear()
	if request.method == "POST":
		name = request.form.get("name")
		roomcode = request.form.get("roomcode")
		join = request.form.get("join", False)
		create = request.form.get("create", False)
		
		if not name:
			return render_template("home.html", error="Enter name.", roomcode = roomcode, name=name)
		
		if len(name) > 10:
			name = name[:11]
		
		new_name = ""
		for c in name:
			if c.isalpha() or c.isdigit():
				new_name += c
		name = new_name

		if join != False and not roomcode:
			return render_template("home.html", error="Enter room code.", roomcode = roomcode, name=name)
		
		room = roomcode.upper()
		if create != False:
			room = generate_code()
			rooms[room] = {"members": 0, "players": []}
			print(room)
		elif roomcode.upper() not in rooms:
			return render_template("home.html", error="Room doesn't exist.", roomcode = roomcode, name=name)
		
		if name in rooms[room]["players"]:
			
			return render_template("home.html", error="Player with same username already in room.<br>You may try entering with a different name.", roomcode = roomcode, name=name)
			

		session["room"] = room
		session["name"] = name
		print(rooms)
		return redirect(url_for("views.room"))

	return render_template("home.html")

@views.route('/room')
def room():
	room = session.get("room")
	return render_template("room.html", code=room)
	
