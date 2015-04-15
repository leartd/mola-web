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
	// Get the user's coordinates (nixed; unreliable)
	// if (latitude == null || longitude == null)
	// {
		// navigator.geolocation is our fallback, because getCurrentPosition is highly unreliable
		// if (navigator.geolocation){
			// var geoOptions = {
				// maximumAge:15000,
				// timeout:10000
			// }
			// navigator.geolocation.getCurrentPosition(success, error, geoOptions);
		// }
		
		// function success(position) {
			// latitude = position.coords.latitude; 
			// longitude = position.coords.longitude;
			// alert(latitude + ", " + longitude);
		// }
		// function error(err) {
			// alert("Error: " + err.code);
		// }
	// }
	
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
				// var locTags = [];
				// for (var j=0; j < loc.locTags.length; j++)
					// locTags.append(loc.locTags[0]);
				createInfoWindow(marker, map, loc.name, loc.url, loc.locTags)
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
function createInfoWindow(marker, map, name, url, locTags){
	var tagsHTML = "";
	for (var i=0; i < locTags.length; i++) {
		tagsHTML += "<span class=\"tag-static well\"><span class=\"tag-text-static\">";
		tagsHTML += locTags[i].type;
		tagsHTML += "</span><span class=\"tag-buttons-static\">";
		if (locTags[i].votes_pos > 0 && locTags[i].votes_pos > locTags[i].votes_neg)
			tagsHTML += "<a class=\"tag-btn-static glyphicon glyphicon-chevron-up tag-pos-selected\"></a>";
		if (locTags[i].votes_neg > 0 && locTags[i].votes_neg > locTags[i].votes_pos)
			tagsHTML += "<a class=\"tag-btn-static glyphicon glyphicon-chevron-down tag-neg-selected\"></a>";
		tagsHTML += "</span></span>";
	}
	try {
		infoContent = "<h4><a href=\"/location/" + url + "\">" + name + "</a></h4>" +
						"<div>" + tagsHTML + "</div>";
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

// Refresh the map.
$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
	refreshMap();
});

function refreshMap() {
	google.maps.event.trigger(map, 'resize');
	var latlng = new google.maps.LatLng(parseFloat(latitude), parseFloat(longitude));
	map.setCenter(latlng);
}
	
if((window.location.pathname).match("/location/.*")){
	google.maps.event.addDomListener(window, 'load', locationMap);
}
if((window.location.pathname) == ("/")){
	google.maps.event.addDomListener(window, 'load', mainPageMap);
}