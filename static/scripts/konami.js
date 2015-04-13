
var secret ="38384040373937396665";
// var secret ="3838";
var secretFound = false;
var input = "";
var timer;
//The following function sets a timer that checks for user input. You can change the variation in how long the user has to input by changing the number in ‘setTimeout.’ In this case, it’s set for 500 milliseconds or ½ second.
$(document).keyup(function(e) {
   input += e.which;    
   clearTimeout(timer);
   timer = setTimeout(function() { input = ""; }, 500);
   check_input();
});
//Once the time is up, this function is run to see if the user’s input is the same as the secret code
function check_input() {
    if(input == secret && secretFound == false) {
    	$('body').css('background-image', 'url(/static/images/inconspicuous.jpg)');
    	secretFound = true;         
    }
};