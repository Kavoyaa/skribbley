var socketio = io()

const messages = document.getElementById("messages");
const players = document.getElementById("players");

const update_player_list = (player_list) => {
    new_player_list_html = ""
    player_list.forEach(function(item) {
        new_player_list_html += `${item}\n`
    })

    players.innerHTML = new_player_list_html


}

const create_message = (name, message, cause, player_list) => {
    if (cause == "player connect" || cause == "player disconnect") {
        update_player_list(player_list)
        
        messages.innerHTML = `<div class="msg"><b>${name}</b> ${message}</div>\n` + messages.innerHTML;
    }
    else {
        messages.innerHTML = `<div class="msg"><b>${name}</b> ${message}</div>\n` + messages.innerHTML; 
    }


};

socketio.on("message", (data) => {
    create_message(data.name, data.message, data.cause, data.player_list)
})


message_field = document.getElementById("message")
message_field.onkeypress = function(e) {
    var keyCode = e.code || e.key;
    if (keyCode == 'Enter'){
        if (message_field.value == "") {return}
        socketio.emit("message", {data: message_field.value})
        
        message_field.value = "";
    }
}
