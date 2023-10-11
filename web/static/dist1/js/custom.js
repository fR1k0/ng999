$(function () {
  "use strict";

  // Feather Icon Init Js
  feather.replace();

  $(".preloader").fadeOut();

  $(".left-sidebar").hover(
    function () {
      $(".navbar-header").addClass("expand-logo");
    },
    function () {
      $(".navbar-header").removeClass("expand-logo");
    }
  );
  // this is for close icon when navigation open in mobile view
  $(".nav-toggler").on("click", function () {
    $("#main-wrapper").toggleClass("show-sidebar");
    $(".nav-toggler i").toggleClass("ti-menu");
  });
  $(".nav-lock").on("click", function () {
    $("body").toggleClass("lock-nav");
    $(".nav-lock i").toggleClass("mdi-toggle-switch-off");
    $("body, .page-wrapper").trigger("resize");
  });
  $(".search-box a, .search-box .app-search .srh-btn").on("click", function () {
    $(".app-search").toggle(200);
    $(".app-search input").focus();
  });

  // ==============================================================
  // Right sidebar options
  // ==============================================================
  $(function () {
    $(".service-panel-toggle").on("click", function () {
      $(".customizer").toggleClass("show-service-panel");
    });
    $(".page-wrapper").on("click", function () {
      $(".customizer").removeClass("show-service-panel");
    });
  });
  // ==============================================================
  // This is for the floating labels
  // ==============================================================
  $(".floating-labels .form-control")
    .on("focus blur", function (e) {
      $(this)
        .parents(".form-group")
        .toggleClass("focused", e.type === "focus" || this.value.length > 0);
    })
    .trigger("blur");

  // ==============================================================
  //tooltip
  // ==============================================================
  $(function () {
    var tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  });
  // ==============================================================
  //Popover
  // ==============================================================
  $(function () {
    var popoverTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl);
    });
  });

  // ==============================================================
  // Perfact scrollbar
  // ==============================================================
  $(".message-center, .customizer-body, .scrollable").perfectScrollbar({
    wheelPropagation: !0,
  });

  /*var ps = new PerfectScrollbar('.message-body');
    var ps = new PerfectScrollbar('.notifications');
    var ps = new PerfectScrollbar('.scroll-sidebar');
    var ps = new PerfectScrollbar('.customizer-body');*/

  // ==============================================================
  // Resize all elements
  // ==============================================================
  $("body, .page-wrapper").trigger("resize");
  $(".page-wrapper").delay(20).show();

  // ==============================================================
  // To do list
  // ==============================================================
  $(".list-task li label").click(function () {
    $(this).toggleClass("task-done");
  });

  // ==============================================================
  // Collapsable cards
  // ==============================================================
  $('a[data-action="collapse"]').on("click", function (e) {
    e.preventDefault();
    $(this)
      .closest(".card")
      .find('[data-action="collapse"] i')
      .toggleClass("ti-minus ti-plus");
    $(this).closest(".card").children(".card-body").collapse("toggle");
  });
  // Toggle fullscreen
  $('a[data-action="expand"]').on("click", function (e) {
    e.preventDefault();
    $(this)
      .closest(".card")
      .find('[data-action="expand"] i')
      .toggleClass("mdi-arrow-expand mdi-arrow-compress");
    $(this).closest(".card").toggleClass("card-fullscreen");
  });
  // Close Card
  $('a[data-action="close"]').on("click", function () {
    $(this).closest(".card").removeClass().slideUp("fast");
  });
  // ==============================================================
  // LThis is for mega menu
  // ==============================================================
  $(".mega-dropdown").on("click", function (e) {
    e.stopPropagation();
  });
  // ==============================================================
  // Last month earning
  // ==============================================================
  $("#monthchart").sparkline([5, 6, 2, 9, 4, 7, 10, 12], {
    type: "bar",
    height: "35",
    barWidth: "4",
    resize: true,
    barSpacing: "4",
    barColor: "#1e88e5",
  });
  $("#lastmonthchart").sparkline([5, 6, 2, 9, 4, 7, 10, 12], {
    type: "bar",
    height: "35",
    barWidth: "4",
    resize: true,
    barSpacing: "4",
    barColor: "#7460ee",
  });
  var sparkResize;

  // ==============================================================
  // This is for the innerleft sidebar
  // ==============================================================
  $(".show-left-part").on("click", function () {
    $(".left-part").toggleClass("show-panel");
    $(".show-left-part").toggleClass("ti-menu");
  });

  // For Custom File Input
  $(".custom-file-input").on("change", function () {
    //get the file name
    var fileName = $(this).val();
    //replace the "Choose a file" label
    $(this).next(".custom-file-label").html(fileName);
  });
});


  // ==============================================================
  // Call Alert
  // ==============================================================
// Succesful alert showing up
function showAlert(text) {
  $('#success-alert').addClass('show').removeClass('hide');
  $('#success-alert span').text(text);

  // Closing the alert after 5 seconds
  setTimeout(function () {
      $('#success-alert').addClass('hide').removeClass('show');
  }, 5000);
}

// Day modal interactions
$('#dayModal #changeDay').on('change', function() {
  $('#dayModal .error-text').removeClass('hide');
  $('#dayModal .modal-footer').removeClass('hide');
});

$('#dayModal button[type="submit"]').on('click', function() {
  var newDay = $('#dayModal #changeDay').val();
  $('#dayModal').modal('hide');
  $('#dayModal .error-text').addClass('hide');
  $('#dayModal .modal-footer').addClass('hide');
  showAlert(`Successfully changed to Day ${newDay}`);
});

// Zone modal interactions
$('#zoneModal button[type="submit"]').on('click', function() {
  $('#zoneModal').modal('hide');
  showAlert('Have successfully change the zone');
});

// Add Items interactions
$('#addItemsModal .add-stage-btn').on('click', function() {
  $('#addItemsModal .add-stage:first')
    .clone()
    .append('<div class="delete-stage"><span class="material-symbols-rounded">delete</span></div>')
    .appendTo('#more-stages');
});

// Delete created stage
$(document).on('click', '#addItemsModal .delete-stage', function(){
    $(this).closest('.add-stage').remove();
});

// Datepicker init
$('input[name="daterange"]').daterangepicker();