async function getLobbyHTML(){
    var lobbyhtml = await (await fetch('lobby.html')).text()
    document.getElementById('lobby-div-target').innerHTML = lobbyhtml
}
getLobbyHTML()


socket.on('lobby-update', (res) =>{
    // Clean every child
    console.log(res)
    var targetNode = document.getElementById('lobby-players-targets')
    while (targetNode.firstChild) {
        targetNode.removeChild(targetNode.lastChild);
    }

    // Insert new child for every response
    for (var property in res) {
        var element = document.createElement('li')
        element.classList.add('list-group-item');
        element.innerHTML = property + '-' + res[property]
        targetNode.appendChild(element)
    }
})
