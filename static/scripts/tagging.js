var tags = ["supercalifragilistic ", "wheelchair", "braille", "understanding", "autism"];
var tags_text = ["placeholder", "wheelchair-friendly", "blind-friendly", "understanding", "autism-friendly"];	

function getCaret(el) { 
  if (el.selectionStart) { 
    return el.selectionStart; 
  } else if (document.selection) { 
    el.focus(); 

    var r = document.selection.createRange(); 
    if (r == null) { 
      return 0; 
    } 

    var re = el.createTextRange(), 
        rc = re.duplicate(); 
    re.moveToBookmark(r.getBookmark()); 
    rc.setEndPoint('EndToStart', re); 

    return rc.text.length; 
  }  
  return 0; 
}

function checkWord(textArea) {
    position = getCaret(textArea);
    text = textArea.value.slice(0, position);
    text_replaced = text.replace(/[\.,-\/#!$%\^&\*;:{}=\_`~()\r\n]/g,' ');
    last_word = text_replaced.trim().split(' ').reverse()[0];

    if (tags.indexOf(last_word.toLowerCase()) > -1) {
    	var indexOfTag = tags.indexOf(last_word.toLowerCase());
        var newTag = "<span class='tag well'><span class='tag-text'>" + tags_text[indexOfTag] + "</span><span class='tag-buttons'><a class='tag-btn tag-pos glyphicon glyphicon-chevron-up'></a><a class='tag-btn tag-neg glyphicon glyphicon-chevron-down'></a><a class='tag-btn tag-cancel glyphicon glyphicon glyphicon-remove'></a></span></span>";
	    console.log(last_word);

	    var flagForTag = 0;
            $("#current_post_tags").children(".tag").each(function(){
                console.log($(this).text() +"TEXT");
        	if ($(this).text() == tags_text[indexOfTag])
        		flagForTag = 1;
        });

        if (flagForTag == 0)
        	$("#current_post_tags").append(newTag);
    }
}

$('#review_text').keyup(function(event){
    event = event || window.event;
    var key = event.keyCode || ev.which;
    if (String.fromCharCode(key).match(/[\.,-\/#!$%\^&\*;:{}=\_`~() \r\n]/)) {
                checkWord(this);
                // console.log(this);
   }
});



$('.review-text').keyup(function(event){
	event = event || window.event;
	var key = event.keyCode || ev.which;
	if (String.fromCharCode(key).match(/[\.,-\/#!$%\^&\*;:{}=\_`~() \r\n]/)) {
                checkWord(this);
                // console.log(this);
   }
});

$("#current_post_tags").on('click', '.tag-btn', function (e) {
		console.log('this is the click ' + $(this).parent().siblings(".tag-text").text());
		e.preventDefault();	

    	var thisTag = $(this, ".tag-btn.tag-pos").parent().closest(".tag");
    	var thisTagText = $(thisTag).children(".tag-text").text();
    	var tagValue = tags_text.indexOf(thisTagText.toLowerCase());

    if ($(this).hasClass("tag-pos")){
        $(this, ".tag-btn.tag-pos").toggleClass("tag-pos-checked");
        if($(this, ".tag-btn.tag-pos").hasClass("tag-pos-checked")){
        	$("#"+thisTagText+"-tag").remove();

        	if($(this).siblings(".tag-neg-checked"))
	    		$(this).siblings(".tag-neg-checked").toggleClass("tag-neg-checked");

        	var inputForTag = "<input type='hidden' name='tags' value='"+ tagValue+"' id='"+ thisTagText +"-tag'>";
        	thisTag.append(inputForTag);
        }
        else{
        	console.log("#"+thisTagText+"-tag");
        	$("#"+thisTagText+"-tag").remove();
        }
    }
    if ($(this).hasClass("tag-neg")){
	    $(this, ".tag-btn.tag-neg").toggleClass("tag-neg-checked");
	    if($(this, ".tag-btn.tag-neg").hasClass("tag-neg-checked")){
	    	$("#"+thisTagText+"-tag").remove();

	    	if($(this).siblings(".tag-pos-checked"))
	    		$(this).siblings(".tag-pos-checked").toggleClass("tag-pos-checked");

        	var inputForTag = "<input type='hidden' name='tags' value='" + "-" + tagValue+"' id='"+ thisTagText +"-tag'>";
        	thisTag.append(inputForTag);
        }
        else{
        	console.log("#"+thisTagText+"-tag");
        	$("#"+thisTagText+"-tag").remove();
        }
    }
    if ($(this).hasClass("tag-cancel")){
	    $(this, ".tag-btn.tag-cancel").toggleClass("tag-cancel-checked");
	    $(this).closest(".tag").remove();
    }    
});
