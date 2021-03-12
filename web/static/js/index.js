const socket = io()

document.getElementById('joinlobby').addEventListener('click',() => {
    var value = document.getElementById('usernameEntry').value
    socket.emit('join-lobby',value)
})

document.getElementById('leavelobby-button').addEventListener('click',() => {
    displayLobbyJoin();
    socket.emit('leave-lobby')
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
    displayLobbyStatus()
    let myusername = document.getElementById('usernameEntry').value;
})



function displayLobbyJoin(){
    document.getElementById('lobby-join-menu').style.display = 'block'
    document.getElementById('lobby-display-menu').style.display = 'none'
    document.getElementById('panorama').style.display = 'none'
    document.getElementById('leaderboard-container').style.display = 'none'

    document.getElementById('lobby-card-container').style.display = 'block'

    document.title = 'Lobby'
}

function displayLobbyStatus(){
    document.getElementById('lobby-join-menu').style.display = 'none'
    document.getElementById('lobby-display-menu').style.display = 'block'
    document.getElementById('panorama').style.display = 'none'

    document.getElementById('lobby-card-container').style.display = 'block'
    document.getElementById('leaderboard-container').style.display = 'none'

    document.title = 'Lobby'
}

function displayPanorama(){
    document.getElementById('lobby-card-container').style.display = 'none'

    document.getElementById('lobby-join-menu').style.display = 'none'
    document.getElementById('lobby-display-menu').style.display = 'none'
    document.getElementById('panorama').style.display = 'block'
    document.getElementById('leaderboard-container').style.display = 'none'

    document.title = 'Biza\'s Pano Guesser'
}

function displayScoreboard(){
    document.getElementById('lobby-card-container').style.display = 'none'

    document.getElementById('lobby-join-menu').style.display = 'none'
    document.getElementById('lobby-display-menu').style.display = 'none'
    document.getElementById('panorama').style.display = 'none'

    document.getElementById('leaderboard-container').style.display = 'grid'
    document.title = 'Biza\'s Pano Guesser'
}
