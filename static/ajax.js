$(document).ready(function() {
  $.ajaxSetup({ cache: false,
                async: true });

  $('button#forward').bind('click', function() {
    $.ajax({
      url: '/forward'
    });
  });

  $('button#stop').bind('click', function() {
    $.ajax({
      url: '/stop'
    });
  });

  $('button#backward').bind('click', function() {
    $.ajax({
      url: '/backward'
    });
  });

  $('button#takePic').bind('click', function() {
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
    $.ajax({
      url: '/record_vid'
    });
  });

});
