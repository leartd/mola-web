function setup() { 
    $(".review-text").attr('readonly', true);
    $(".hidden-button").attr("style", "visibility:hidden;");
    $(".set-review").rateit('readonly', true);
}
function make_editable(post_id) {
    var current = $("#" + post_id + " textarea").attr("readonly");
    var display = current ? "visibility:normal;" : "visibility:hidden;"
    $("#" + post_id + " textarea").attr("readonly", !current);
    $("#" + post_id + " .hidden-button").attr("style", display);
    $(".set-review").rateit('readonly', !$(".set-review").rateit("readonly"));
};