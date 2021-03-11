let userinfo = {}

let myusername = 'Notrichi' // Update username on round entry

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


function doCountdown(countDownDate){
    // Update the count down every 1 second
    var CountDownInterval = setInterval(function() {

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

      // If the count down is finished, write some text
      if (distance < 0) {
        clearInterval(CountDownInterval);
        document.getElementById("countDownDisplay").innerHTML = "EXPIRED";
      }
    }, 1000);
}


var seconds = 90
doCountdown(new Date(Date.now() + seconds*1000))

const sampleLeaderboard = {'Mike Towers' : 1000, 'Notrichi': 200, 'Fucking God!': 1500}
const samplecolorboard = {'Mike Towers' : 'brown', 'Notrichi': 'black', 'Fucking God!': 'yellow'}
updateLeaderboard(sampleLeaderboard, samplecolorboard)


function updateLeaderboard(leaderjson, colorsjson, endLeaderboard = false){ //self.scores maps 'username' -> score
    // Sorts scores descendentally


    var sorted = Object.entries(leaderjson).sort(([,b],[,a]) => a-b).reduce((r, [k, v]) => ({ ...r, [k]: v }), {});

    var LeaderboardTable = document.getElementById('LeaderboardTable-Body')
    if (endLeaderboard){
        var LeaderboardTable = document.getElementById('end-LeaderboardTable-Body')
    }
    deepClearDelete(LeaderboardTable)

    userinfo['usercolors'] = colorsjson
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
mapModalJquery.find('[data-bs-dismiss="modal"]').click(() =>{
    unlockModalClose()
    mapModalJquery.modal('hide')
    lockModalClose()
});

function lockModalClose() {
    mapModalJquery.on('hide.bs.modal', preventHide);
}

function unlockModalClose() {
    mapModalJquery.off('hide.bs.modal', preventHide);
}

const sampleReveal = {'Mike Towers' : {lat: 45, lng: 56}, 'Notrichi': {lat: 45, lng: 80}, 'Fucking God!': {lat:30 , lng: 56},
'SOLUTION' : {lat: 61.39146458246076 , lng: 15.89755986088935}}
// Receives a json mapped from username -> object of {lat: 45, lng: 45, distance: 2000}
// Also receives an entry called 'SOLUTION', which contains SOL
let revealLayer = L.layerGroup().addTo(mymap);
function revealMap(json){
    // Locks the map in, reveals everything
    var jsoncolors = userinfo['usercolors']

    lockModalClose()
    mapModalJquery.modal('show')

    var rightLocation = json['SOLUTION']
    var rightLocation_marker = L.marker(rightLocation).addTo(revealLayer);

    setTimeout(()=>{
        mymap.off('click', onMapClick); // Disable map guessing
        mymap.removeLayer(playerGuess)// Remove old marker
        var mylist = [rightLocation]
        for (var username in json) {
            if (username !== 'SOLUTION'){
                var playercolor = jsoncolors[username]
                var playerlatlng = json[username]

                lineOpts = {color: playercolor}
                var playerMarker = L.marker(playerlatlng,{icon: MarkerColors[playercolor]}).addTo(revealLayer);

                var geodesic = new L.Geodesic([playerlatlng, rightLocation],lineOpts)
                geodesic.addTo(revealLayer);
                mylist.push(playerlatlng)


                var distance = Math.floor(geodesic.distance(playerlatlng,rightLocation)/1000)

                playerMarker.bindPopup(username + '\n' + distance + 'km')
                if (username == myusername){
                    document.getElementById('mapModalTitle').innerHTML = `You were ${distance} kilometers away!`
                }
            }
        }

        // mymap.fitBounds([rightLocation, mylist[1] ]);
        mymap.fitBounds(mylist)
    },1000)

}

// Cleans everything back to next round as normal
function clearNextRound(){
    mymap.removeLayer(revealLayer)
    mymap.on('click', onMapClick);
    playerGuess.setLatLng([41.56203190200195,-38.87721477590272])
    playerGuess.addTo(mymap)

    unlockModalClose()
    mapModalJquery.modal('hide')
    mymap.setView([0, 0], 2);

    document.getElementById('mapModalTitle').innerHTML = 'Make your Guess!'
}

function setPlayerMarker(color){
    playerGuess.setIcon(MarkerColors[color])
}

var mapModalVar = document.getElementById('mapModal')
mapModalVar.addEventListener('shown.bs.modal', function (event) {
    // setTimeout(function(){ mymap.invalidateSize()}, 200);
    mymap.invalidateSize();
})


function TogglePlayerGuess(){
    var lockguessbutton = document.getElementById('guesslockbutton')
    if (lockguessbutton.innerHTML.includes('Unlock')){
        UnlockPlayerGuess()
    } else {
        LockPlayerGuess()
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

    mymap.on('click', onMapClick); //Disable click move
    lockguessbutton.innerHTML = 'Lock your Guess!'

    // Emit guess unlock
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


var panorama = pannellum.viewer('panorama', {
    "type": "equirectangular",
    "panorama": "/panos/currentPano.png?00001",
    "autoLoad": true,
    "showFullscreenCtrl": false,
    "showZoomCtrl": false,
});

function reloadPanorama(){
    document.querySelector('#panorama').innerHTML  = ''

    panorama = pannellum.viewer('panorama', {
        "type": "equirectangular",
        "panorama": "/panos/nextPano.png",
        "autoLoad" : true,
        "showFullscreenCtrl": false,
        "showZoomCtrl": false,
    });

}
