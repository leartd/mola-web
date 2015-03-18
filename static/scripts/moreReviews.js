$('.more_reviews').click(function(event){
	event.preventDefault();
	$("a.more_reviews").attr("href", "");
	var count_reviews = $('.reviews').length;

	var loc_id = $('#loc_id').val();

	if(reviewsDBFlag == true){
		$.ajax({
			type: "GET",
			url: "../get/reviews?id=" + loc_id + "&dbPage=" + reviewsDBPage,
			async: true,

			success: function(data){
				// alert(data);
				var obj = JSON.parse(data);
				//define Json, get Reviews object
				//update reviewsDBPage = json.dbasfsd;
				$('#loc-page-reviews').append(obj.reviews);
				reviewsDBPage = obj.reviewsCursor;
				reviewsDBFlag = obj.reviewsDBFlag;
			},
			error: function(XMLHttpRequest, textStatus, errorThrown){
				alert("Ajax error");
				$('.more_reviews').text('No more reviews.');
			}
		});
	}
	else{
		$('.more_reviews').text('No more reviews.');
		// $('.more_reviews').prop('disabled', true);
	}
});