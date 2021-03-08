var socket = io()

document.getElementById('joinlobby').addEventListener('click',() => {
    var value = document.getElementById('usernameEntry').value
    socket.emit('join-lobby',value)
})

//  A message is received
socket.on("message", data => {
  var messagedisplay = document.getElementById('lobby-join-messagetext')
  messagedisplay.style.color = 'red';
  messagedisplay.innerHTML = data;
});

socket.on('invalid-join', ()=>{
    document.getElementById('usernameEntry').value = '';
})

socket.on('valid-join',()=>{
    document.getElementById('lobby-join-menu').style.display = 'none'
    document.getElementById('lobby-display-menu').style.display = 'block'
})