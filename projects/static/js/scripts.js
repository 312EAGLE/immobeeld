// OPEN VIDEO OVERLAY ON CLICK

$('#play-video').on('click', function(e){
  e.preventDefault();
  $('#video-overlay').addClass('open');
  $("#video-overlay").append('<iframe width="560" height="315" src="https://www.youtube.com/embed/drq41E_2rDU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>');
});

$('.video-overlay, .video-overlay-close').on('click', function(e){
  e.preventDefault();
  close_video();
});

$(document).keyup(function(e){
  if(e.keyCode === 27) { close_video(); }
});

function close_video() {
  $('.video-overlay.open').removeClass('open').find('iframe').remove();
};


// Calculation services
$(document).ready(function() {
  // Get the checkbox elements
  var checkboxes = $('input[name="services"]');
  
  // Calculate and update the total price on change
  checkboxes.on('change', function() {
    var totalPrice = 0;
    checkboxes.each(function() {
      if ($(this).is(':checked')) {
        var servicePrice = parseFloat($(this).siblings('.service-price').text().replace('€', ''));
        totalPrice += servicePrice;
      }
    });
    var totalExclVat = totalPrice.toFixed(2);
    var totalInclVat = (totalPrice * 1.21).toFixed(2);
    $('#total-price').text('Total Price (Excl. VAT): €' + totalExclVat + ' | Total Price (Incl. VAT): €' + totalInclVat);
  });
});