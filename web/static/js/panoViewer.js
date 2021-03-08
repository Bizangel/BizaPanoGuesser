// var socket = io();
//
// document.querySelector('.minus').addEventListener('click',(event)=>{
//     socket.emit('minus')
// })
//
// document.querySelector('.plus').addEventListener('click',(event)=>{
//     socket.emit('plus')
// })
//
// socket.on('stateupdate', function(received) {
//   value = document.querySelector('.value')
//   value.textContent = received
// });
//
// socket.on('connectedupdate', function(received) {
//   users = document.querySelector('.users')
//   users.textContent = received + ' Connected'
// });

// pannellum.viewer('panorama', {
//     "type": "equirectangular",
//     "panorama": "/panos/nextPano.png"
// });

var panorama = pannellum.viewer('panorama', {
    "type": "equirectangular",
    "panorama": "/panos/currentPano.png",
    "autoLoad": true,
    "showFullscreenCtrl": false,
});

function nextPanorama(){
    document.querySelector('#panorama').innerHTML  = ''

    panorama = pannellum.viewer('panorama', {
        "type": "equirectangular",
        "panorama": "/panos/nextPano.png",
        "autoLoad" : true,
        "showFullscreenCtrl": false,
    });

}


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

var playerIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const playerGuess = L.marker([51.5, -0.09],{icon: playerIcon}).addTo(mymap);
function onMapClick (e) {
  playerGuess.setLatLng(e.latlng);
}

mymap.on('click', onMapClick);


var mapModal = document.getElementById('mapModal')
mapModal.addEventListener('show.bs.modal', function (event) {
    setTimeout(function(){ mymap.invalidateSize()}, 500);
})


const solLat = 61.39146458246076
const solLong = 15.89755986088935

function debug(){
    revealMap(solLat,solLong)
}

const playerColor = '#fcf403'

function revealMap(lat, long){
    var playerlatlng = playerGuess.getLatLng()

    var rightLocation = {lat: lat, lng: long};
    var rightLocation_marker = L.marker([lat, long]).addTo(mymap);

    lineOpts = {color: playerColor}
    var geodesic = new L.Geodesic([playerlatlng, rightLocation],lineOpts).addTo(mymap);
    mymap.fitBounds([rightLocation,playerlatlng]);
}
