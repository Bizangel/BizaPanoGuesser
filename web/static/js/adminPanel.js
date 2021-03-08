var socket = io();

const AdminToken = document.getElementById('tokenHolder').getAttribute('token')

// Remove yourself from game-Count
socket.emit('leave-lobby')

document.getElementById('debugButton').addEventListener('click',(e)=>{
    socket.emit('admin-debug',{pwd: AdminToken})
})
