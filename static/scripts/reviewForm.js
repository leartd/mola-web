function setup() { 
    $(".review-text").attr('readonly', true);
    $(".hidden-button").attr("style", "visibility: hidden;");
    $(".set-review").rateit('readonly', true);
}
function make_editable(post_id) {
    var current = $("#" + post_id + " textarea").attr("readonly");
    var display = current ? "visibility:normal;" : "visibility:hidden;"
    $("#" + post_id + " textarea").attr("readonly", !current);
    $("#" + post_id + " .hidden-button").attr("style", display);
    $("#" + post_id + " .set-review").rateit('readonly', !$("#" + post_id + " .set-review").rateit("readonly"));

    //TAG Editing messy
    // var editable_post_children = $("#"+post_id).find(".tag-btn");
    // if(editable_post_children.hasClass("tag-pos-selected")){
    // 	alert(editable_post_children);	
    // 	editable_post_children.addClass("tag-pos-checked");
    // 	editable_post_children.toggleClass("tag-pos-selected");
    // }
    // if(editable_post_children.hasClass("tag-neg-selected")){
    // 	editable_post_children.addClass("tag-neg-checked");
    // 	editable_post_children.toggleClass("tag-neg-selected");
    // }
};