const mapboxAccessToken = 'pk.eyJ1IjoibHZzeiIsImEiOiJjam9qOXIzdTYwMnFpM2t2d2MyaHJxcXJsIn0.EBOtf2ATioNXLSCXj2DxGQ'
// VUB
var start = L.latLng(50.8227, 4.3950);
// Grand Place
var dest = L.latLng(50.84656, 4.3526);

// create the map
var map = L.map('map').setView(dest,5);
var marker = L.marker(start);

function userLocation(e) {
    start = e.latlng;
    map.setView(start,15);
    //marker.setLatLng(e.latlng).addTo(map);
    control.setWaypoints([start, dest]);
}

map.on('locationfound', userLocation).setView(start,15).locate();

// create tile layer for map
L.tileLayer(`https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=${mapboxAccessToken}`, {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 19,
    id: 'mapbox.streets',
}).addTo(map);

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
}).addTo(map);

map.on('click', function(e) {
    console.log("hello");
    var container = L.DomUtil.create('div'),
        // startBtn = createButton('Start from this location', container),
        destBtn = createButton('Go to this location', container);

    L.popup()
        .setContent(container)
        .setLatLng(e.latlng)
        .openOn(map);

    L.DomEvent.on(destBtn, 'click', function() {
        control.spliceWaypoints(
            control.getWaypoints().length - 1, 1, e.latlng);
        map.closePopup();
    });
});

var venue_markers = L.layerGroup().addTo(map);

$('#find-nearby-venues').click(function() {
    const point = map.getCenter();
    const lng = point.lng;
    const lat = point.lat;
    $.get('/webtech/user_locate/', {lng: point.lng, lat: point.lat}, function(data) {
        const venues = JSON.parse(data);
        for (venue of venues) {
            var marker = L.marker(venue.latLng, {
                title: venue.name,
                alt: venue.name,
                riseOnHover: true,
            })
                .on({'click': function(e){control.spliceWaypoints(control.getWaypoints().length - 1, 1, e.latlng)}})
                .addTo(venue_markers);
        };
    });
});

var event_markers = L.layerGroup().addTo(map);

function event_marker_content(evt) {
    var html = `<p class="event-marker">${evt.date}: ${evt.name}<br>`;
    html += `${evt.weekday}, ${evt.time} @ ${evt.venue}<br>`;
    html += 'line-up:<ul>';
    for (artist of evt.artists) {
        html += `<li>${artist.name}</li>`;
    };
    html += '</ul></p>';
    return html;
}

function get_events_on_date(dateString, inst) {
    if (dateString) {
        event_markers.clearLayers();
        const dateList = dateString.split('/');
        $.get( '/webtech/events_on_date/',
            { dd: dateList[0], mm: dateList[1], yy: dateList[2] },
            function(data) {
                const evts = JSON.parse(data);
                for (evt of evts) {
                    var popup = L.popup({
                        closeButton: false,
                        autoClose: false,
                        closeOnEscapeKey: false,
                        closeOnClick: false,
                    })
                        .setLatLng(evt.latLng)
                        .setContent(event_marker_content(evt))
                        .addTo(event_markers);
                }
            })
    }
};

$( function() {
    $( "#datepicker" ).datepicker({
        dateFormat: "dd/mm/yy",
        onClose: get_events_on_date,
    });
});
