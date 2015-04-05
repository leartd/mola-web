var tags = ["ramp", "braille", "understanding", "autism"];
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
        console.log(last_word);
        // instead of logging, go to the proper tag checkbox and check it
        // then when a checkbox is checked there's going to be a jquery function that will
        // add the correct tag to the view.
        // once the tag has been noted and value designated then the javascript will 
        // give the checkbox the correct "value" i.e. -1 or 1 or 0 if tag is annulled
    }
}

$('#review_text').keyup(function(event){
	event = event || window.event;
	var key = event.keyCode || ev.which;
	if (String.fromCharCode(key).match(/[\.,-\/#!$%\^&\*;:{}=\_`~() \r\n]/)) {
                checkWord(this);
   }
});