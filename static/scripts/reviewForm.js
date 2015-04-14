// var tags = ["supercalifragilistic ", "wheelchair", "braille", "understanding", "autism"];
// var tags_text = ["placeholder", "wheelchair-friendly", "blind-friendly", "understanding", "autism-friendly"];   

var tags_array = {};
// getCurrentTags();

function getCurrentTags(){
    tags_array = {};
    var present_tags = $("#current_post_tags").children(".tag");
    for( var j = 0; j < present_tags.length; j++){
        var tag_in_review = $(present_tags[j]).children(".tag-text").text();
        var this_tags_value = tags_text.indexOf(tag_in_review);
        console.log($(present_tags[j]).children(".tag-text").text());
        $(present_tags[j]).children().children(".tag-btn").each(function(){
            if($(this).hasClass("tag-pos-selected")){
               console.log("positive");               
            }
           else if ($(this).hasClass("tag-neg-selected")){
            console.log("negative");
                this_tags_value = 0 - this_tags_value;
            }
        });
        tags_array[tag_in_review] = this_tags_value;
    }    
}

function setup() { 
    $(".review-text").attr('readonly', true);
    $(".hidden-button").attr("style", "display:none;");
    $(".set-review").rateit('readonly', true);
    getCurrentTags();
}
function make_editable(post_id) {
    var current = $("#" + post_id + " textarea").attr("readonly");
    var display = current ? "display:normal;" : "display:none;"
    $("#" + post_id + " textarea").attr("readonly", !current);
    $("#" + post_id + " .hidden-button").attr("style", display);
    $(".set-review").rateit('readonly', !$(".set-review").rateit("readonly"));

    // console.log(current);
    if(current){
        if(! $.isEmptyObject(tags_array)){
            var present_tags = $("#current_post_tags").children(".tag");
            present_tags.remove();
            checkAllWords($("#" + post_id + " textarea"));
                
        }
        else{
            console.log("There are no tags in this review.");
        }
    }
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

function checkAllWords(textArea) {
    text = textArea.val();
    text_replaced = text.replace(/[\.,-\/#!$%\^&\*;:{}=\_`~()\r\n]/g,' ');
    // last_word = text_replaced.trim().split(' ').reverse()[0];
    text_array = text_replaced.trim().split(' ');
    text_array_length = text_array.length;

    for( var i = 0; i < text_array_length; i++){
        last_word = text_array[i];

        if (tags.indexOf(last_word.toLowerCase()) > -1) { 
            var indexOfTag = tags.indexOf(last_word.toLowerCase());
            var newTag = "<span class='tag well'><span class='tag-text'>" + tags_text[indexOfTag] + "</span><span class='tag-buttons'><a class='tag-btn tag-pos glyphicon glyphicon-chevron-up'></a><a class='tag-btn tag-neg glyphicon glyphicon-chevron-down'></a><a class='tag-btn tag-cancel glyphicon glyphicon glyphicon-remove'></a></span></span>";
            console.log(last_word);

            var flagForTag = 0;

            $(".tag-text").each(function(){
                if ($(this).text() == tags_text[indexOfTag])
                    flagForTag = 1;
            });

            if (flagForTag == 0)
                $("#current_post_tags").append(newTag);
        }

    }
    // End of For-loop
}