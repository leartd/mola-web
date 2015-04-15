var marker;

//=============================================================================
// locationMap draws a Google Map on a Location Page.
//=============================================================================
function locationMap() {
	// Get the location's coordinates.
	try {
		var coords = new google.maps.LatLng(latitude, longitude);
	}
	catch(err) {
		return;
	}
	
	// Set the map options. Interactivity for Location Page maps should be
	// minimal.
	var mapOptions = {
		zoom: 17,
		center: coords,
		disableDefaultUI: true,
		disableDoubleClickZoom: false,
		draggable: true,
		keyboardShortcuts: true,
		maxZoom: 19,
		minZoom: 15,
		panControl: true,
		rotateControl: false,
		scaleControl: true,
		scrollwheel: true,
		streetViewControl: false,
		zoomControl: true
	}
	var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

	var curMarker = createMarker(coords, map, name);
	// createInfoWindow(curMarker, map, name, url);
}

//=============================================================================
// mainPageMap draws a Google Map on the Main Page with location Markers.
//=============================================================================
var map;
function mainPageMap() {
	// Get the user's coordinates.
	if (latitude == null || longitude == null)
	{
		// navigator.geolocation is our fallback, because getCurrentPosition is highly unreliable
		if (navigator.geolocation){
			var geoOptions = {
				maximumAge:15000,
				timeout:10000
			}
			navigator.geolocation.getCurrentPosition(success, error, geoOptions);
		}
		
		function success(position) {
			latitude = position.coords.latitude; 
			longitude = position.coords.longitude;
			alert(latitude + ", " + longitude);
		}
		function error(err) {
			alert("Error: " + err.code);
		}
	}
	
	try {
		var userCoords = new google.maps.LatLng(latitude, longitude);
	}
	catch(err) {
		return;
	}
	
	// Set the map options. Interactivity for Location Page maps should be
	// minimal.
	var mapOptions = {
		zoom: 15,
		center: userCoords,
		disableDefaultUI: true,
		disableDoubleClickZoom: false,
		draggable: true,
		keyboardShortcuts: true,
		maxZoom: 19,
		minZoom: 13,
		panControl: true,
		rotateControl: false,
		scaleControl: true,
		scrollwheel: true,
		streetViewControl: false,
		zoomControl: true
	}
	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
		
	// Populate the main page map with markers and InfoWindows.
	$.ajax({
		type: "GET",
		url: "../get/nearby_locations?" +
			"latitude=" + latitude +
			"&longitude=" + longitude,
		async: true,

		success: function(data){
			var obj = JSON.parse(data);
			// Add markers and InfoWindows.
			for (var i=0; i < obj.locations.length; i++) {
				var loc = (obj.locations[i]);
				var coords = new google.maps.LatLng(parseFloat(loc.latitude), parseFloat(loc.longitude));
				marker = createMarker(coords, map, "ann");
				createInfoWindow(marker, map, loc.name, loc.url)
			}
		},
		error: function(XMLHttpRequest, textStatus, errorThrown){
			console.log("AJAX Error!");
		}
	});
	;
}

// Create a marker for a location.
function createMarker(coords, map, name){
	var marker = new google.maps.Marker({
		position: coords,
		map: map,
		title: name
	});
	return marker;
}

// Create an InfoWindow for a marker.
function createInfoWindow(marker, map, name, url){
	// alert(tags);
	try {
		infoContent = "<h5><a href=\"/location/" + url + "\">" + name + "</a></h5>";
						// "<div>" + tags + "</div>";
	}
	catch(err) {
		return;
	}
	var info = new google.maps.InfoWindow({
		content: infoContent
	});
	google.maps.event.addListener(marker, 'click', function() {
		// map.setCenter(marker.position);
		info.open(map, this);
	});
}

if((window.location.pathname).match("/location/.*")){
	google.maps.event.addDomListener(window, 'load', locationMap);
}
if((window.location.pathname) == ("/")){
	google.maps.event.addDomListener(window, 'load', mainPageMap);
}