// This example displays an address form, using the autocomplete feature
// of the Google Places API to help users fill in the information.

var placeSearch, autocomplete;
var componentForm = {
  street_number: 'short_name',
  route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'short_name',
  country: 'long_name',
  placeName: 'place_name',
  placeID: 'place_id'
  // postal_code: 'short_name'
};
submit=false;

function initialize() {

  $("#autocomplete")[0].value = "";
  for (var component in componentForm) {
    document.getElementById(component).value = '';
    // document.getElementById(component).disabled = false;
  }

  // Create the autocomplete object, restricting the search
  // to geographical location types.
  autocomplete = new google.maps.places.Autocomplete(
      /** @type {HTMLInputElement} */(document.getElementById('autocomplete')),
      { types: ['establishment'] });
  // When the user selects an address from the dropdown,
  // populate the address fields in the form.
  google.maps.event.addListener(autocomplete, 'place_changed', function() {
    fillInAddress();
  });

  $("#search_form").submit(function(e) { 
      if (document.getElementById('placeID').value=="") { 
        e.preventDefault(); 
      } 
  });
  // var form = document.getElementById('search_form');
  // form.addEventListener('onSubmit', function(e) {
  //   if ($('.pac-container:visible').length) {
  //     return false;
  //   }
  // });
}

// [START region_fillform]
function fillInAddress() {
  submit = true;
  // Get the place details from the autocomplete object.
  var place = autocomplete.getPlace();
  console.log(place)
  for (var component in componentForm) {
    document.getElementById(component).value = '';
    // document.getElementById(component).disabled = false;
  }

  // Get each component of the address from the place details
  // and fill the corresponding field on the form.
  for (var i = 0; i < place.address_components.length; i++) {
    var addressType = place.address_components[i].types[0];
    if (componentForm[addressType]) {
      var val = place.address_components[i][componentForm[addressType]];
      document.getElementById(addressType).value = val;
    }
  }
  document.getElementById('placeName').value = place.name;
  console.log(place.name);
  document.getElementById('placeID').value = place.place_id;
  $("#search_form").submit()
}
// [END region_fillform]

// [START region_geolocation]
// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = new google.maps.LatLng(
          position.coords.latitude, position.coords.longitude);
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}
// [END region_geolocation]
