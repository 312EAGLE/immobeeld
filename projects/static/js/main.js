var currentTab = 0;
showTab(currentTab);
// Function that updates the total price
function updateTotalPrice() {
  var checkboxes = $('input[name="services"]');
  checkboxes.on('change', function() {
    var totalPrice = 0;
    checkboxes.each(function() {
      if ($(this).is(':checked')) {
        var labelText = $(this).siblings('label').text();
        var servicePrice = parseFloat(labelText.split('€')[1].trim());
        if (!isNaN(servicePrice)) {
          totalPrice += servicePrice;
        }
      }
    });
    var totalExclVat = totalPrice.toFixed(2);
    var totalInclVat = (totalPrice * 1.21).toFixed(2);
    $('#total-price').text('Total Price (Excl. VAT): €' + totalExclVat + ' | Total Price (Incl. VAT): €' + totalInclVat);
  });
}

function showTab(n) {
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";

  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit"; // changes the Next button to Submit on the last step
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  fixStepIndicator(n)

  // Call the updateTotalPrice function every time the second tab becomes active
  if (n == 1) {
    updateTotalPrice();
    $('#total-price').show(); // Show the total price
  } else {
    $('#total-price').hide(); // Hide the total price
  }
}

function nextPrev(n) {
  var x = document.getElementsByClassName("tab");

  // If you are at the end of the form, submit the form
  if (currentTab == x.length - 1 && n > 0) {
    document.getElementById("orderForm").submit();
    return false;
  }

  // Otherwise, hide the current tab and go to the next/previous one
  x[currentTab].style.display = "none";
  currentTab = currentTab + n;

  // Then display the next tab
  showTab(currentTab);
}

function fixStepIndicator(n) {
  var i, x = document.getElementsByClassName("single-step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  x[n].className += " active done";
}

document.getElementById("prevBtn").addEventListener("click",function(e) {
  var i, x = document.getElementsByClassName("single-step");
  for (i = 1; i < x.length; i++) {
    if(x[i].classList.contains("done")) {
      x[i].classList.remove("done");
    }
  }
});


$(document).ready(function () {
  $('#dtHorizontalVerticalExample').DataTable({
    "scrollX": true,
    "scrollY": 200,
  });
  $('.dataTables_length').addClass('bs-select');
});

