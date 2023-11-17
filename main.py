from website import create_app, create_socket
from flask_socketio import join_room, leave_room, send, SocketIO
from flask import session
from website.views import rooms	

app = create_app()
socketio = create_socket(app)

@socketio.on("connect")
def connect(auth):
	room = session.get("room")
	name = session.get("name")

	if not room or not name:
		return
	if room not in rooms:
		return
	
	rooms[room]["members"] += 1
	rooms[room]["players"].append(name)
	
	join_room(room)
	send({"name": name, "message": "joined the room.", "cause": "player connect", "player_list":rooms[room]["players"]}, to=room)


@socketio.on("disconnect")
def disconnect():
	room = session.get("room")
	name = session.get("name")
	
	rooms[room]["players"].append(name)
	leave_room(room)

	if room in rooms:
		rooms[room]["members"] -= 1
		if rooms[room]["members"] <= 0:
			del rooms[room]
			
	
	send({"name": name, "message": "left the room.", "cause": "player disconnect", "player_list":rooms[room]["players"]}, to=room)


@socketio.on("message")
def message(data):
	room = session.get("room")
	name = session.get("name")
	
	send({"name": name+":", "message": data["data"], "cause": "chat message sent"}, to=room)

#if __name__ == '__main__':
#	socketio.run(app, debug=True)
