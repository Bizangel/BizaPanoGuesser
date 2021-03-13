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


let AdminToken = null;
let verifiedHost = false;
function HostConnect(){
    const adminsocket = io('/admin');

    adminsocket.on('message',(mess) =>{
        document.getElementById("messageholder").innerHTML = mess
    })

    // document.getElementById('debugButton').addEventListener('click',(e)=>{
    //     adminsocket.emit('admin-debug',{pwd: AdminToken})
    // })

    document.getElementById('pano-enqueue-button').addEventListener('click',(e)=>{
        adminsocket.emit('admin-pano-enqueue',{pwd: AdminToken})
    })


    document.getElementById('startGame').addEventListener('click',(e)=>{
        var totalrounds = document.getElementById("totalrounds").value
        var roundduration = document.getElementById("roundduration").value
        adminsocket.emit('admin-startGame',{pwd: AdminToken,
            totalrounds: totalrounds, round_duration: roundduration})
    })


    document.getElementById('setPanoParams').addEventListener('click',(e)=>{
        var urban = document.getElementById("urban").checked
        var indoors = document.getElementById("indoors").checked
        var countryNumber = document.getElementById("countryNumber").value

        if (!countryNumber){
            countryNumber = null;
        }

        adminsocket.emit('admin-setPanoParams', {pwd: AdminToken, urban :  urban,
        indoors: indoors, countryNumber: countryNumber})
    })

    document.getElementById('hostnextroundbutton').addEventListener('click',(e)=>{
        adminsocket.emit('admin-nextRound',{pwd: AdminToken})
    })


    document.getElementById('claimHostButton').addEventListener('click',(e) =>{
        var token = document.getElementById('adminkeyinput').value
        adminsocket.emit('verify-admin-token', {pwd: token})
    })

    adminsocket.on('admin-verify', (token) =>{
                AdminToken = token
                verifiedHost = true;
                document.getElementById('admin-claim').style.display = 'none'
                document.getElementById('admin-display').style.display = 'block'
                document.getElementById('hostnextroundbutton').style.display = 'block'
    })
}
