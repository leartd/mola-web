var map;

//=============================================================================
// locationMap draws a Google Map on a Location Page.
//=============================================================================
function locationMap() {
	// Get the coordinates.
	var coords = new google.maps.LatLng(latitude, longitude);
	
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
		minZoom: 12,
		panControl: true,
		rotateControl: false,
		scaleControl: true,
		scrollwheel: true,
		streetViewControl: false,
		zoomControl: true
	}
	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

	var curMarker = createMarker(coords, map, name);
	
	// Keep the center of the map at the location, even after resizing.
	// google.maps.event.addDomListener(window, 'resize', function() {
		// map.setCenter(coords);
	// });
}

// Create a marker and infowindow for a location.
function createMarker(coords, map, name){
	// Create the actual marker.
	var marker = new google.maps.Marker({
		position: coords,
		map: map,
		title: name
	});
	// Create the associated InfoWindow.
	infoContent = "<h4>" + name + "</h4>"
	var info = new google.maps.InfoWindow({
		content: infoContent
	});
	google.maps.event.addListener(marker, 'click', function() {
		info.open(map, this);
	});
	
	return marker;
}

google.maps.event.addDomListener(window, 'load', locationMap);