const mapboxAccessToken = 'pk.eyJ1IjoibHZzeiIsImEiOiJjam9qOXIzdTYwMnFpM2t2d2MyaHJxcXJsIn0.EBOtf2ATioNXLSCXj2DxGQ'
// Grand Place
var dest = L.latLng(50.8467139, 4.3524994);
// Brussels Central Station
var user_location = L.latLng(50.8454639, 4.3569867);

// create the map
var map = L.map('map').setView(dest,5);


// routing plugin
var control = L.Routing.control({
    router: L.Routing.mapbox(mapboxAccessToken, { profile: 'mapbox/walking' })
}).addTo(map);

// create tile layer for map
L.tileLayer(`https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=${mapboxAccessToken}`, {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 19,
    id: 'mapbox.streets',
}).addTo(map);

var venue_markers = L.layerGroup().addTo(map);

function addVenueMarker(venue) {
    return marker = L.marker(venue.latlng, {
        title: venue.name,
        alt: venue.name,
        riseOnHover: true,
    })
        .on({'click': function() {updateRoute(venue)} })
        .addTo(venue_markers);
}


function userLocation(e) {
    user_location = e.latlng;
    control.setWaypoints([user_location, dest]);
}


$( document ).ready(function() {
    const venue = JSON.parse(document.getElementById("venue-info").innerHTML);
    dest = venue.latlng;
    addVenueMarker(venue);
    map.setView(venue.latlng, 15);
    map.on('locationfound', userLocation).locate()
});

