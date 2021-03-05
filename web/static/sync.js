// <script>
//     var minus = document.querySelector('.minus'),
//         plus = document.querySelector('.plus'),
//         value = document.querySelector('.value'),
//         users = document.querySelector('.users'),
//         websocket = new WebSocket("ws://127.0.0.1:5005/");
//     minus.onclick = function (event) {
//         websocket.send(JSON.stringify({action: 'minus'}));
//     }
//     plus.onclick = function (event) {
//         websocket.send(JSON.stringify({action: 'plus'}));
//     }
//     websocket.onmessage = function (event) {
//         data = JSON.parse(event.data);
//         switch (data.type) {
//             case 'state':
//                 value.textContent = data.value;
//                 break;
//             case 'users':
//                 users.textContent = (
//                     data.count.toString() + " user" +
//                     (data.count == 1 ? "" : "s"));
//                 break;
//             default:
//                 console.error(
//                     "unsupported event", data);
//         }
//     };
// </script>

var socket = io();

document.querySelector('.minus').addEventListener('click',(event)=>{
    socket.emit('minus')
})

document.querySelector('.plus').addEventListener('click',(event)=>{
    socket.emit('plus')
})

socket.on('stateupdate', function(received) {
  value = document.querySelector('.value')
  value.textContent = received
});

socket.on('connectedupdate', function(received) {
  users = document.querySelector('.users')
  users.textContent = received + ' Connected'
});

// document.querySelector('.minus').addEventListener('click',(event)=>{
//
// })

// socket.emit('minus');
// input.value = '';
