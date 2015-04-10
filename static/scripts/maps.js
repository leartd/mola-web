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
		disableDoubleClickZoom: true,
		draggable: true,
		keyboardShortcuts: false,
		maxZoom: 19,
		minZoom: 15,
		panControl: true,
		rotateControl: false,
		scaleControl: true,
		scrollwheel: false,
		streetViewControl: false,
		zoomControl: true
	}
	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

	// Set the marker on the location.
	var marker = new google.maps.Marker({
		position: coords,
		map: map,
		title: "{{ name }}"
	});
	
	// Keep the center of the map at the location, even after resizing.
	google.maps.event.addDomListener(window, 'resize', function() {
		map.setCenter(coords);
	});
}

google.maps.event.addDomListener(window, 'load', locationMap);