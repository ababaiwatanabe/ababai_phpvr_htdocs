jQuery(document).ready(function($){
	$('.get_station').click(function(){
		var txtArea = $('.result_station:first');
		var cord = $('.cord:first').val().split(',');
		$.getJSON("http://express.heartrails.com/api/json?method=getStations&x=" + cord[1] + "&y=" + cord[0],null, function(data){
			alert('ok');

		});
	});
});
