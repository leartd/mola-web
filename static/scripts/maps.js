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
	// createInfoWindow(curMarker, map, name, address);
	
	// Keep the center of the map at the location, even after resizing.
	// google.maps.event.addDomListener(window, 'resize', function() {
		// map.setCenter(coords);
	// });
}

//=============================================================================
// mainPageMap draws a Google Map on the Main Page with location Markers.
//=============================================================================
function mainPageMap() {
	// Get the user's coordinates.
	alert("mainPageMap() called");
	try {
		var userCoords = new google.maps.LatLng(latitude, longitude);
	}
	catch(err) {
		alert("That ain't good");
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
	var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
	
	// var curMarker = createMarker(coords, map, name);
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
function createInfoWindow(marker, map, name, address){
	try {
		infoContent = "<h5>" + name + "</h5>";
		if(address)
			infoContent += "<div>" + address + "</div>";
	}
	catch(err) {
		return;
	}
	var info = new google.maps.InfoWindow({
		content: infoContent
	});
	google.maps.event.addListener(marker, 'click', function() {
		info.open(map, this);
	});
}

if((window.location.pathname).match("/location/.*")){
	google.maps.event.addDomListener(window, 'load', locationMap);
}
if((window.location.pathname) == ("/")){
	google.maps.event.addDomListener(window, 'load', mainPageMap);
}