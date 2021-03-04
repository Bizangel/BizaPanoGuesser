const mapbox_public_token = 'pk.eyJ1IjoiYml6YW5nZWwiLCJhIjoiY2tscWtuYzJnMDE5aTJwbTc4Nms5dGw1aCJ9.gIsDo80nwpvQZIT36f8Tqg';
const mymap = L.map('mapid').setView([51.505, -0.09], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 18,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: mapbox_public_token
}).addTo(mymap);

// const popup = L.popup();

// function onMapClick (e) {
//   popup
//     .setLatLng(e.latlng)
//     .setContent('You clicked the map at ' + e.latlng.toString())
//     .openOn(mymap);
// }

// mymap.on('click', onMapClick);
const marker = L.marker([51.5, -0.09]).addTo(mymap);
function onMapClick (e) {
  marker
    .setLatLng(e.latlng);
}

mymap.on('click', onMapClick);

// marker.bindPopup('<b>Hello world!</b><br>I am a popup.').openPopup();
