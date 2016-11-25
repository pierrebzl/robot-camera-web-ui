$(document).ready(function() {
  $.ajaxSetup({ cache: false,
                async: true });
});


$(function() {
	$('button#Avancer').bind('click', function() {
		$.getJSON($SCRIPT_ROOT + '/Avancer', function(data, item){
	         $( "#result" ).text(data.result);
	      });
	    return false;
	});
});

$(function() {
	$('button#Reculer').bind('click', function() {
		$.getJSON($SCRIPT_ROOT + '/Reculer', function(data, item){
	         $( "#result" ).text(data.result);
	      });
	    return false;
	});
});