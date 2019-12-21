document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    console.log(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        document.querySelector('#form').onsubmit = function() {
            const message_text = document.querySelector('#message_text').value;
            console.log(message_text);
            socket.emit('new message', {'message_text': message_text});
        };
    });

    // When a new vote is announced, add to the unordered list
    socket.on('messages', data => {
      console.log("da5l")
      const li = document.createElement('li');
      li.innerHTML = `Vote recorded: ${data}`;
      document.querySelector('#messages').append(li);
    });
});
