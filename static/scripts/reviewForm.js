// var tags = ["supercalifragilistic ", "wheelchair", "braille", "understanding", "autism"];
// var tags_text = ["placeholder", "wheelchair-friendly", "blind-friendly", "understanding", "autism-friendly"];   

var tags_array = {};
var original_tags = $("#current_post_tags").children(".tag");
// getCurrentTags();

function getCurrentTags(){
    var present_tags = $("#current_post_tags").children(".tag");
    for( var j = 0; j < present_tags.length; j++){
        var tag_in_review = $(present_tags[j]).children(".tag-text").text();
        var this_tags_value = 0; 
        console.log($(present_tags[j]).children(".tag-text").text());
        $(present_tags[j]).children().children(".tag-btn").each(function(){
            if($(this).hasClass("tag-pos-selected")){
               this_tags_value = tags_text.indexOf(tag_in_review);
               console.log("positive");               
            }
           if ($(this).hasClass("tag-neg-selected")){
                console.log("negative");
                this_tags_value = 0 -  tags_text.indexOf(tag_in_review);
            }
        });
        tags_array[tag_in_review] = this_tags_value;
    }    
}

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
    
    if((window.location.pathname) == ("/history")){
        // alert("I'm the history page");
        if(current){
            // console.log(post_id + " This is the post id");
            // $("#review_text-" +post_id).attr()
            $(".reviews_assoc_tags-" + post_id).attr("id", "current_post_tags");
            // $(".reviews_assoc_tags-agxkZXZ-bW9sYS12ZWJyEwsSBlJldmlldxiAgICAgMjjCAw")
        }
        else{
            $(".reviews_assoc_tags-" + post_id).attr("id", "");
        }
    }
    // console.log(current);
    tags_array = {};
    getCurrentTags(post_id);
    if(current){
        if(! $.isEmptyObject(tags_array)){
            var present_tags = $("#current_post_tags").children(".tag");
            present_tags.remove();
            checkAllWords($("#" + post_id + " textarea"));
            present_tags = $("#current_post_tags").children(".tag");
            // $( document ).ready(function() {
                // present_tags = $("#current_post_tags").closest(".tag");
            // });

            for(var i = 0; i < present_tags.length; i++){
                var text_from_tag = $(present_tags[i]).children(".tag-text").text();
                if(tags_array[text_from_tag]){
                    console.log(tags_array[text_from_tag]);
                    if(tags_array[text_from_tag] > 0){
                        console.log("DETECTING POSITIVE BUTTON");
                       console.log(present_tags[i]);
                       console.log($(present_tags[i]).children(".tag-buttons").children(".tag-pos")[0].click());
                        // tagButton.click();
                    }
                    if(tags_array[text_from_tag] < 0){
                        console.log("DETECTING NEGATIVE BUTTON");
                       console.log(present_tags[i]);
                       console.log($(present_tags[i]).children(".tag-buttons").children(".tag-neg")[0].click());
                        // tagButton.click();
                    }
                    // if(tags_array[text_from_tag] < 0){
                    //     console.log("DETECTING NEGATIVE BUTTON");
                    //     console.log(present_tags[i]);
                    //     console.log("");
                    //     var temporary = $(present_tags[i]);

                    //     // $(present_tags[i]).children(".tag-buttons").children(".tag-neg")[0].click();
                    //     // $(present_tags[i]).children(".tag-buttons").children(".tag-neg").trigger("click");
                    //     // tagButton.clcik();
                    // }
                }
            }    
        }
        else{
            console.log("There are no tags in this review.");
        }
    }
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
