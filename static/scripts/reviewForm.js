function setup() { 
    $(".review-text").attr('readonly', true);
    $(".hidden-button").attr("style", "visibility:hidden;");
    $(".rating-input").prop('disabled', true);
    $(".rating-input").attr('style', 'cursor:default;');
}
function make_editable(post_id) {
    var current = $("#" + post_id + " textarea").attr("readonly");
    var display = current ? "visibility:normal;" : "visibility:hidden;"
    $("#" + post_id + " textarea").attr("readonly", !current);
    $("#" + post_id + " .hidden-button").attr("style", display);
    $("#" + post_id + " .review-section").toggleClass("rating");
    $(".rating-input").prop('disabled', function(i, v) { return !v; })
};