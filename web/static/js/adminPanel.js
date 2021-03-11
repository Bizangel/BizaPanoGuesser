var socket = io('/admin');

const AdminToken = document.getElementById('tokenHolder').getAttribute('token')

document.getElementById('debugButton').addEventListener('click',(e)=>{
    socket.emit('admin-debug',{pwd: AdminToken})
})

document.getElementById('startGame').addEventListener('click',(e)=>{
    socket.emit('admin-startGame',{pwd: AdminToken})
})
