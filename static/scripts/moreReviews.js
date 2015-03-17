$('a.more_reviews').click(function(){
	var count_reviews = $('.reviews').length;
	var loc_id = $('#loc_id').val();
	$.ajax({
		type: "GET",
		url: "../get/reviews?id=" + loc_id + "&offset=" + count_reviews,
		async: true,

		success: function(data){
			// alert(data);
			$('#loc-page-reviews').append("<h1>"+data+"</h1>");
		},
		error: function(XMLHttpRequest, textStatus, errorThrown){
			alert("it didn't");
		}
	});
});