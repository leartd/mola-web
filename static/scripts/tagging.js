var tags = ["wheelchair", "braille", "understanding", "autism"];
var tags_text = ["wheelchair-friendly", "blind-friendly", "understanding", "autism-friendly"];	

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

        $(".tag-text").each(function(){
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
   }
});


$("#current_post_tags").on('click', '.tag-btn', function (e) {
		console.log('this is the click ' + $(this).parent().siblings(".tag-text").text());
		e.preventDefault();	
    if ($(this).hasClass("tag-pos")){
        // "li", "li.item-ii"
        $(this, ".tag-btn.tag-pos").css('background-color','#00B16A');
        $(this, ".tag-btn.tag-pos").css('color','#fff');
        // add hidden input here
    }
    if ($(this).hasClass("tag-neg")){
	    // "li", "li.item-ii"
	    $(this, ".tag-btn.tag-neg").css('background-color','#EF4836');
	    $(this, ".tag-btn.tag-neg").css('color','#fff');
	    // add hidden input here

    }
    if ($(this).hasClass("tag-cancel")){
	    // "li", "li.item-ii"
	    $(this, ".tag-btn.tag-neg").css('background-color','#666');
	    $(this, ".tag-btn.tag-neg").css('color','#fff');    
	    $(this).closest(".tag").remove();
    }    
});
