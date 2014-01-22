$(".btn-group a").hover(function () {
  $(this).addClass("btn");
  }, function () {
    $(this).removeClass("btn");
  }
);

// Fill meal on add serving modal
$(document).on("click", ".open-add-serving", function () {
     var meal = $(this).data('meal');
     $(".modal-body #meal").val(meal);
});