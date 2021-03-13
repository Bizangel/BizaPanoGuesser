const colors = {
    'aqua': '#18f4fe',
    'black':'#434343',
    'blue':'#358acd',
    'brown':'#aa5a3e',
    'deep_blue':'#0507ff',
    'green':'#33b22c',
    'orange':'#ff7617',
    'purple':'#9b31cd',
    'red':'#ce3a4f',
    'yellow':'#cec53a',
}

// How to fetch an HTML asynchronizally, not really needed here
// async function getLobbyHTML(){
//     var lobbyhtml = await (await fetch('lobby.html')).text()
//     document.getElementById('lobby-div-target').innerHTML = lobbyhtml
// }
// getLobbyHTML()


socket.on('lobby-update', (res) =>{
    // Clean every child
    // console.log(res)
    var targetNode = document.getElementById('lobby-players-targets')
    while (targetNode.firstChild) {
        targetNode.removeChild(targetNode.lastChild);
    }

    // Insert new child for every response
    for (var username in res) {
        var element = document.createElement('li')
        element.classList.add('list-group-item');
        // element.innerHTML = username + '-' + res[property]
        element.innerHTML = `
        ${username} <span class="badge" style="background-color: ${colors[res[username]]};">${res[username]}</span>
        `
        targetNode.appendChild(element)
    }
})

socket.on('game-starting-soon', ()=>{
    document.getElementById('waithost-message').innerHTML = 'Host has started the game! It will start soon...'
})
