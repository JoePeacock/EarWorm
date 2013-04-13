function put(data) {
	return $.ajax({
	        type: "GET",
	        url: "/search/query",
	        data: data,	           
	});
}

$(document).ready(function() {
	$("#appendedInputButton").keyup(function() {
		put("q=" + $(this).val()).complete(function(xhr, textStatus) {
			var res = JSON.parse(xhr.responseText);
			console.log(res[0]['url']);
			$('#results').empty();
			for (i =0; i < 5; i++) {
				if (res[i] != null) {
					$('#results').append('<li><div class="row"><div class="span2"><img src="' + res[i]['img'] + '" width="100"></div><div class="span10"><a href="'+ res[i]['url'] + '" target="_blank">' + res[i]['title'] + '</a></div></div></li>');
				}
			}	 
	    });  
	});		
});
