function checkFields(form_button) {
    var form_object = $("#loc_form");
    var name=$("#name_loc_form")[0];
    var addr=$("#address_loc_form")[0];
    var city=$("#city_loc_form")[0];
    var state=$("#state_loc_form")[0];

    var valid_form = true;
    if (name.value == "") {
        name.className = name.className + " form-error"
        valid_form = false;
    }
    if (addr.value == "") {
        addr.className = addr.className + " form-error"
        valid_form = false;
    }
    if (city.value == "") {
        city.className = city.className + " form-error"
        valid_form = false;
    }
    if (state.value == "") {
        state.className = state.className + " form-error"
        valid_form = false;
    }
    if (valid_form) {
        form_object.submit()
    }
    else {
        $("#error-text")[0].style.display="block"
    }
}

function removeError(ele) {
    ele.className = ele.className.replace( /(?:^|\s)form-error(?!\S)/g , '' )
}