const mapboxAccessToken = 'pk.eyJ1IjoibHZzeiIsImEiOiJjam9qOXIzdTYwMnFpM2t2d2MyaHJxcXJsIn0.EBOtf2ATioNXLSCXj2DxGQ'
// VUB
var start = L.latLng(50.8227, 4.3950);
// Grand Place
var dest = L.latLng(50.84656, 4.3526);

// create the map
var mymap = L.map('mapid').setView(dest,5);
var marker = L.marker(start);

function userLocation(e) {
    start = e.latlng;
    mymap.setView(start,15);
    //marker.setLatLng(e.latlng).addTo(mymap);
    control.setWaypoints([start, dest]);
}

mymap.on('locationfound', userLocation).setView(start,15).locate();

// create tile layer for mymap
L.tileLayer(`https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=${mapboxAccessToken}`, {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 19,
    id: 'mapbox.streets',
}).addTo(mymap);

// routing plugin
function createButton(label, container) {
    var btn = L.DomUtil.create('button', 'a', container);
    btn.setAttribute('type', 'button');
    btn.innerHTML = label;
    return btn;
}

var control = L.Routing.control({
    // waypoints: [ start, dest ],
    router: L.Routing.mapbox(mapboxAccessToken, { profile: 'mapbox/walking' })
    //router: new L.Routing.osrmv1({serviceUrl: '//router.project-osrm.org/viaroute', profile: 'foot'})
}).addTo(mymap);

mymap.on('click', function(e) {
    console.log("hello");
    var container = L.DomUtil.create('div'),
        // startBtn = createButton('Start from this location', container),
        destBtn = createButton('Go to this location', container);

    L.popup()
        .setContent(container)
        .setLatLng(e.latlng)
        .openOn(mymap);

    L.DomEvent.on(destBtn, 'click', function() {
        control.spliceWaypoints(
            control.getWaypoints().length - 1, 1, e.latlng);
        mymap.closePopup();
    });
});
