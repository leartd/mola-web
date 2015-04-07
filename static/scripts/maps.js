//=============================================================================
// initializeMap draws a Google Map on the current page.
//=============================================================================
var map;

function initializeMap() {
	var coords = new google.maps.LatLng(-34.397, 150.644);
	var mapOptions = {
		zoom: 15,
		center: coords,
		panControl: false
	}
	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

	google.maps.event.addDomListener(map, 'idle', function() {
	  calculateCenter();
	});

	var marker = new google.maps.Marker({
		position: coords,
		map: map,
		title: "{{ name }}"
	});
}

//=============================================================================
// calculateCenter always keeps a Google Map on the page centered.
//=============================================================================
var center;

function calculateCenter() {
  center = map.getCenter();
}

google.maps.event.addDomListener(window, 'resize', function() {
  map.setCenter(center);
});

google.maps.event.addDomListener(window, 'load', initializeMap);