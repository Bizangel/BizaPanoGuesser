let userinfo = {}


const mapbox_public_token = 'pk.eyJ1IjoiYml6YW5nZWwiLCJhIjoiY2tscWtuYzJnMDE5aTJwbTc4Nms5dGw1aCJ9.gIsDo80nwpvQZIT36f8Tqg';
// const mymap = L.map('mapid').setView([51.505, -0.09], 13);
const mymap = L.map('mapid').setView([0, 0], 2);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 18,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: mapbox_public_token
}).addTo(mymap);



const playerGuess = L.marker([41.56203190200195,-38.87721477590272],{icon: markerAqua}).addTo(mymap);
function onMapClick (e) {
  playerGuess.setLatLng(e.latlng);
}
mymap.on('click', onMapClick);


let CountDownInterval = null
function doCountdown(countDownDate){
    // Update the count down every 1 second
    CountDownInterval = setInterval(function() {

      // Get today's date and time
      var now = new Date().getTime();

      // Find the distance between now and the count down date
      var distance = countDownDate - now;

      // Time calculations for days, hours, minutes and seconds
      // var days = Math.floor(distance / (1000 * 60 * 60 * 24));
      // var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);

      var totalseconds = minutes*60 + seconds
      // Display the result in the element with id="demo"
      document.getElementById("countDownDisplay").innerHTML = totalseconds +  "s ";
      if (totalseconds < 30){
          document.getElementById("countDownDisplay").classList.remove("bg-primary")
          document.getElementById("countDownDisplay").classList.add("bg-danger")
      }

      if(!CurrentlyLocked){
          // Background emit
          if(totalseconds == 1 || totalseconds == 2){
              // Do background emit
              console.log('background emit!')
              var latlng = playerGuess.getLatLng()
              socket.emit('guess-lock-background', {'lat': latlng.lat, 'lng': latlng.lng})
          }
      }

      // If the count down is finished, write some text
      if (distance < 0) {
        clearInterval(CountDownInterval);
        document.getElementById("countDownDisplay").innerHTML = "0s";
      }
    }, 1000);
}


// var seconds = 90
// doCountdown(new Date(Date.now() + seconds*1000))
//
// const sampleLeaderboard = {'Mike Towers' : 1000, 'Notrichi': 200, 'Fucking God!': 1500}
// const samplecolorboard = {'Mike Towers' : 'brown', 'Notrichi': 'black', 'Fucking God!': 'yellow'}
// updateLeaderboard(sampleLeaderboard, samplecolorboard)


function updateLeaderboard(leaderjson, endLeaderboard = false){ //self.scores maps 'username' -> score
    // Sorts scores descendentally


    var sorted = Object.entries(leaderjson).sort(([,b],[,a]) => a-b).reduce((r, [k, v]) => ({ ...r, [k]: v }), {});

    var LeaderboardTable = document.getElementById('LeaderboardTable-Body')
    if (endLeaderboard){
        var LeaderboardTable = document.getElementById('end-LeaderboardTable-Body')
    }
    deepClearDelete(LeaderboardTable)

    var colorsjson = userinfo['usercolors']
    var i = 1
    for (var username in sorted) {
        var score = leaderjson[username]
        var tablerow = document.createElement('tr')
        var usercolor = colors[colorsjson[username]]
        var number = document.createElement('th')
        var userdisplay = document.createElement('td')
        var userscoredisplay = document.createElement('td')

        if (!endLeaderboard){
            var notcheck = document.createElement('td')
        }


        number.setAttribute('scope','row')
        number.innerHTML = i;
        userdisplay.innerHTML = username;

        userscoredisplay.innerHTML = score;

        number.style.color = usercolor;
        userdisplay.style.color = usercolor;
        userscoredisplay.style.color = usercolor;

        if (!endLeaderboard){
            notcheck.innerHTML = `
            <i class="fas fa-times" id="checkmark-${username}"></i>
            `
            notcheck.style.color = usercolor;
        }



        tablerow.appendChild(number)
        tablerow.appendChild(userdisplay)
        tablerow.appendChild(userscoredisplay)
        if (!endLeaderboard){
            tablerow.appendChild(notcheck)
        }


        LeaderboardTable.appendChild(tablerow)
        i++;
    }
}

function updateCheckState(username,state){
    // State either true CHECKED, user is username
    if (state){
        document.getElementById('checkmark-' + username).className = 'fas fa-check';
    }
    else{
        document.getElementById('checkmark-' + username).className = 'fas fa-times'
    }
}


let mapModalJquery = $('#mapModal');

function preventHide(e) {
    e.preventDefault();
}

// if you have buttons that are allowed to close the modal
function setButtonsLock(){
    mapModalJquery.find('[data-bs-dismiss="modal"]').click(() =>{
        unlockModalClose()
        mapModalJquery.modal('hide')
        lockModalClose()
    });
}

function setButtonsUnlock(){
    mapModalJquery.find('[data-bs-dismiss="modal"]').click(() =>{
        unlockModalClose()
        mapModalJquery.modal('hide')
    });
}

function lockModalClose() {
    mapModalJquery.on('hide.bs.modal', preventHide);
}

function unlockModalClose() {
    mapModalJquery.off('hide.bs.modal', preventHide);
}


function RevealLockGuessButton(){
    var guesslock = document.getElementById('guesslockbutton')
    guesslock.innerHTML = 'Waiting for host...'
    guesslock.className = 'btn btn-primary'
    guesslock.removeEventListener('click', TogglePlayerGuess)
}

function RevealUnlockGuessButton(){
    var guesslock = document.getElementById('guesslockbutton')
    guesslock.addEventListener('click', TogglePlayerGuess)

    guesslock.className = 'btn btn-primary'
    guesslock.innerHTML = 'Lock your Guess!'
}
// const sampleReveal = {'Mike Towers' : {lat: 45, lng: 56}, 'Notrichi': {lat: 45, lng: 80}, 'Fucking God!': {lat:30 , lng: 56},
// 'SOLUTION' : {lat: 61.39146458246076 , lng: 15.89755986088935}}

// Also receives an entry called 'SOLUTION', which contains SOL
let revealLayer = L.layerGroup().addTo(mymap);
function revealMap(json, scores, location_name, country_name){

    if(verifiedHost){ //Display next button
        document.getElementById('hostnextroundbutton').style.display = 'block'
    }
    // Locks the map in, reveals everything
    var jsoncolors = userinfo['usercolors']
    revealLayer = L.layerGroup().addTo(mymap);
    // Stop the timer
    lockModalClose()
    setButtonsLock()
    RevealLockGuessButton()

    if (document.getElementById("countDownDisplay").innerHTML !== "0s"){
        clearInterval(CountDownInterval);
        document.getElementById("countDownDisplay").innerHTML = "0s";
    }



    mapModalJquery.modal('show')

    var rightLocation = json['SOLUTION']
    var rightLocation_marker = L.marker(rightLocation, {icon: solution_marker}).addTo(revealLayer);

    if (location_name){
        rightLocation_marker.bindPopup(`<b>${location_name} </b><br>${country_name}`).openPopup();
    }
    else{
        var latsol = rightLocation['lat'].toFixed(4)
        var lngsol = rightLocation['lng'].toFixed(4)
        rightLocation_marker.bindPopup(`<b>${latsol}, ${lngsol}$ </b><br>${country_name}`).openPopup();
    }

    setTimeout(()=>{
        mymap.off('click', onMapClick); // Disable map guessing
        mymap.removeLayer(playerGuess)// Remove old marker
        var mylist = [rightLocation]
        for (var username in json) {
            if (username !== 'SOLUTION'){
                var playercolor = jsoncolors[username]
                var playerlatlng = json[username]
                var playerscore = scores[username]
                lineOpts = {color: colors[playercolor]} // The actual #hex
                var playerMarker = L.marker(playerlatlng,{icon: MarkerColors[playercolor]}).addTo(revealLayer);

                var geodesic = new L.Geodesic([playerlatlng, rightLocation],lineOpts)
                geodesic.addTo(revealLayer);
                mylist.push(playerlatlng)


                var distance = Math.floor(geodesic.distance(playerlatlng,rightLocation)/1000)

                playerMarker.bindPopup(`<b>${username} </b> <br> ${distance} km away! <br> ${playerscore} points`)
                if (username == myusername){
                    document.getElementById('mapModalTitle').innerHTML = `You were ${distance} kilometers away! You get ${playerscore} points!`
                    mymap.fitBounds([rightLocation, playerlatlng ]);
                }
            }
        }


        // mymap.fitBounds(mylist)
    },1000)

}

// Cleans everything back to next round as normal
function clearNextRound(){
    mymap.removeLayer(revealLayer)
    mymap.on('click', onMapClick);
    playerGuess.setLatLng([41.56203190200195,-38.87721477590272])
    playerGuess.addTo(mymap)

    unlockModalClose()
    setButtonsUnlock()
    RevealUnlockGuessButton()
    mapModalJquery.modal('hide')
    mymap.setView([0, 0], 2);

    document.getElementById('mapModalTitle').innerHTML = 'Make your Guess!'
    document.getElementById('hostnextroundbutton').style.display = 'none' // Hide host button

    document.getElementById("countDownDisplay").classList.remove("bg-danger")
    document.getElementById("countDownDisplay").classList.add("bg-primary")

}

function setPlayerMarker(color){
    playerGuess.setIcon(MarkerColors[color])
}

var mapModalVar = document.getElementById('mapModal')
mapModalVar.addEventListener('shown.bs.modal', function (event) {
    // setTimeout(function(){ mymap.invalidateSize()}, 200);
    mymap.invalidateSize();
})


let CurrentlyLocked = false
function TogglePlayerGuess(){
    var lockguessbutton = document.getElementById('guesslockbutton')
    if (lockguessbutton.innerHTML.includes('Unlock')){
        UnlockPlayerGuess()
        socket.emit('guess-unlock')
        CurrentlyLocked = false
    } else {
        CurrentlyLocked = true // locked so you don't background emit
        LockPlayerGuess()
        var latlng = playerGuess.getLatLng()
        socket.emit('guess-lock', {'lat': latlng.lat, 'lng': latlng.lng})
    }
}

// Emit guess lock
document.getElementById('guesslockbutton').addEventListener('click', TogglePlayerGuess)

function LockPlayerGuess(){
    var lockguessbutton = document.getElementById('guesslockbutton')
    lockguessbutton.className = 'btn btn-success'
    mymap.off('click', onMapClick); //Disable click move
    lockguessbutton.innerHTML = 'Unlock your Guess'
}

function UnlockPlayerGuess(){
    var lockguessbutton = document.getElementById('guesslockbutton')
    lockguessbutton.className = 'btn btn-primary'

    mymap.on('click', onMapClick); //Enable click move
    lockguessbutton.innerHTML = 'Lock your Guess!'
}

function deepClearDelete(node) {
  while (node.hasChildNodes()) {
    recursiveClear(node.firstChild);
  }
}

function recursiveClear(node) {
  while (node.hasChildNodes()) {
    recursiveClear(node.firstChild);
  }
  node.parentNode.removeChild(node);
}

const panostring1 = 'pano1616024823'
const panostring2 = 'pano1616026829'


const panoramaViewer = pannellum.viewer('panorama', {
    // "type": "multires",
    "autoLoad": true,
    "showFullscreenCtrl": false,
    "showZoomCtrl": false,
    "scenes": {

    }
});


function addNewPano(panostring, round){
    panoramaViewer.addScene('round' + round, {
        "type": "multires",
        "multiRes": {
            "basePath": "/panos/" + panostring,
            "path": "/%l/%s%y_%x",
            "fallbackPath": "/fallback/%s",
            "extension": "jpg",
            "tileResolution": 512,
            "maxLevel": 6,
            "cubeResolution": 8432
        }
    });
}

function loadRoundPano(round){
    panoramaViewer.loadScene('round' + round)
}

//  equirectangular version
// const panoramaViewer = pannellum.viewer('panorama', {
//     "type": "equirectangular",
//     "autoLoad": true,
//     "showFullscreenCtrl": false,
//     "showZoomCtrl": false,
//     "scenes": {
//
//     }
// });
//
// function addNewPano(panostring, round){
//     panoramaViewer.addScene('round' + round, {
//         "type": "equirectangular",
//         "panorama": '/panos/' + panostring
//     });
// }
//
// function loadRoundPano(round){
//     panoramaViewer.loadScene('round' + round)
// }






////// Listener Interactivity
socket.on('leaderboard-update', json => {
    updateLeaderboard(json)
});

socket.on('round-update', json => {
    // Json contains, totalrounds, round, linkedstring and DATE we're counting to
    // console.log('round update called!')
    clearNextRound() // Make sure it's clear and ready to go

    var countdown = new Date(json['countdown']*1000)
    doCountdown(countdown)

    var round = json['round']
    var totalrounds = json['totalrounds']
    document.getElementById('roundDisplay').innerHTML = 'Round ' + round + ' / ' + totalrounds

    addNewPano(json['panostring'],round)
    loadRoundPano(round)
    displayPanorama()
})


socket.on('guess-update',json => {
    updateCheckState(json['user'],json['status'])
})


socket.on('map-reveal', json =>{
    console.log(json['users_guesses'])
    console.log(json['roundscores'])
    revealMap(json['users_guesses'],json['roundscores'], json['loc_name'], json['country_name'])
})
/// Called Once per Game.
socket.on('color-set', json =>{
    // console.log('Colo was set!')
    userinfo['usercolors'] = json
    var mycolor = json[myusername]
    setPlayerMarker(mycolor)
})


socket.on('game-reveal', json => {
    clearNextRound()
    updateLeaderboard(json['endleaderboard'], endLeaderboard = true)

    console.log('Game revealed!')
    console.log(json)

    var winnerfirst = json['first']
    var winnersecond = json['second']
    var winnerthird = json['third']

    var firstname = winnerfirst['username']
    var firstpercent = winnerfirst['scorepercent'] + '%'

    console.log(firstpercent)
    if (!winnersecond){
        var secondname = ''
        var secondpercent = '0%'
    }
    else{
        var secondname = winnersecond['username']
        var secondpercent = winnersecond['scorepercent'] + '%'
    }

    if(!winnerthird){
        var thirdname = ''
        var thirdpercent = '0%'
    } else {
        var thirdname = winnerthird['username']
        var thirdpercent = winnerthird['scorepercent'] + '%'
    }

    document.getElementById('firstname').innerHTML = ` ${firstname} <br> ${json['endleaderboard'][firstname]} Points!`
    document.getElementById('secondname').innerHTML = ` ${secondname} <br> ${json['endleaderboard'][secondname]} Points`
    document.getElementById('thirdname').innerHTML = ` ${thirdname} <br> ${json['endleaderboard'][thirdname]} Points`

    document.getElementById('title-display-body').innerHTML = `
    <i class="fas fa-trophy"></i> ${firstname} <i class="fas fa-trophy"></i>
    `

    document.getElementById('colfirst-container').style.backgroundColor = colors[userinfo['usercolors'][firstname]]
    document.getElementById('colsecond-container').style.backgroundColor = colors[userinfo['usercolors'][secondname]]
    document.getElementById('colthird-container').style.backgroundColor = colors[userinfo['usercolors'][thirdname]]

    if (!winnersecond){
        document.getElementById('secondname').innerHTML = ''
    }
    if (!winnerthird){
        document.getElementById('thirdname').innerHTML = ''
    }
    document.getElementById('colfirst-container').style.height = firstpercent
    document.getElementById('colsecond-container').style.height = secondpercent
    document.getElementById('colthird-container').style.height = thirdpercent


    displayLeaderboardAnimation()
    // Leave the lobby for sake of consistency
    document.getElementById('waithost-message').innerHTML = 'Waiting for the host to start...'
    socket.emit('leave-lobby')
})
// socket.on('colortest', json =>{
//     console.log('Colorrrr test!')
//     console.log(json)
// })
