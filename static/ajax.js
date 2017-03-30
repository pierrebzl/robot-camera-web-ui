$(document).ready(function() {
  $.ajaxSetup({ cache: false,
                async: true });

  $('button#forward').bind('click', function() {
	console.log("click");
    $.ajax({
      url: '/forward'
    });
  });

  $('button#stop').bind('click', function() {
	console.log("click");
    $.ajax({
      url: '/stop'
    });
  });

  $('button#backward').bind('click', function() {
	console.log("click");
    $.ajax({
      url: '/backward'
    });
  });

  $('button#takePic').bind('click', function() {
	console.log("click");
    $.ajax({
      url: '/take_pic',
      success: function(response) {
          document.getElementById("previewPic").src = response;
          var link = document.createElement('a');
          link.href = response;
          link.download = response;
          document.body.appendChild(link);
          link.click();
      },
      error: function(error) {
          console.log(error);
      }
    });
  });

  $('button#recordVid').bind('click', function() {
	console.log("click");
    $.ajax({
      url: '/record_vid'
    });
  });

});


/*$(function() {
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
});*/
