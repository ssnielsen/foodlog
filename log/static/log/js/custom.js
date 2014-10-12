
/**
 * jQuery.browser.mobile (http://detectmobilebrowser.com/)
 *
 * jQuery.browser.mobile will be true if the browser is a mobile device
 *
 **/
(function(a){(jQuery.browser=jQuery.browser||{}).mobile=/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4));})(navigator.userAgent||navigator.vendor||window.opera);

$(function() {
  if(jQuery.browser.mobile) {
    $('#collapse-calendar').collapse('hide');
  }
});

// Update serving-button functionality
function updateServingButtons() {
  if (!jQuery.browser.mobile) {
    $('.btn-group.hover-visible').css('visibility', 'hidden');
    $('tr').hover(function() {
      $(this).find('.btn-group.hover-visible').css('visibility', 'visible');
    }, function() {
      $(this).find('.btn-group').css('visibility', 'hidden');
    });
  }

  $('.remove-serving-button').click( function() {
    var serving = $(this).closest('tr');
    var serving_id = serving.attr('id');
    var url = document.URL + 'serving/remove/';
    $.post(url, {serving_id: serving_id}).done( function(data) {
      serving.remove();
      updateDayInfo();
    });
  });
}

// Show buttons on meal and servings when hovering above it. Only on desktop.
$(function() {
  updateServingButtons();
});


// Fill meal on add serving modal
$(document).on("click", ".open-add-serving", function () {
  var meal = $(this).data('meal');
  $(".modal-body #meal").val(meal);
});


// Fill serving on edit serving modal
$(document).on("click", ".open-edit-serving", function () {
  var serving = $(this).data('serving');
  var amount = $(this).data('amount');
  $(".modal-body #serving_id").val(serving);
  $(".modal-body #edit_amount").val(amount);
  $(".modal-body #edit_amount").select();
});

// Add serving to pastebuffer
$(document).on("click", ".add-to-pastebuffer-button", function() {
  var url = getBaseURL() + "/foodlog/paste/add/";
  var serving_id = $(this).data('serving');
  var data = {serving_id: serving_id};
  $.post(url, data).done( function(data) {
    updatePastebuffer();
  });
});

// Reset paste buffer
$(document).on("click", ".reset-pastebuffer-button", function() {
  var url = getBaseURL() + "/foodlog/paste/reset/";
  $.post(url).done( function(data) {
    updatePastebuffer();
  });
});

// Paste buffer into meal
$(document).on("click", ".paste-from-pastebuffer-button", function() {
  var meal = $(this).data('meal');
  var url = document.URL + "paste/";
  data = {'meal': meal};
  $.post(url, data).done( function(data) {
    for(var i = 0; i < data.length; i++) {
      serving = data[i];
      parsed = JSON.parse(serving);
      serving_obj = JSON.parse(parsed.serving_obj);
      var amount = serving_obj[0].fields.amount;
      var serving_id = serving_obj[0].pk;
      addServingRowToMeal(meal, serving_id, parsed.food_text, amount, parsed.cals);
      updateServingButtons();
    }
    updateDayInfo();
  });
});

// Adds a serving row to a given meal. Used for ajax calls (add servings/paste buffer)
function addServingRowToMeal(meal, serving_id, food_text, amount, cals) {
  var row = '<tr id="' + serving_id + '">' +
              '<td>' + food_text +'&nbsp;&nbsp;' +
                '<div class="btn-group hover-visible">' +
                  '<button type="button" class="open-edit-serving btn btn-default btn-xs" data-toggle="modal" data-target="#edit-serving-modal" data-serving="' + serving_id + '" data-amount="' + amount + '">' +
                    '<span class="glyphicon glyphicon-edit"></span>' +
                  '</button>' +
                  '<button type="button" class="add-to-pastebuffer-button btn btn-default btn-xs" data-serving="' + serving_id + '">' +
                    '<span class="glyphicon glyphicon-floppy-save"></span>' +
                  '</button>' +
                  '<button type="button" class="remove-serving-button btn btn-default btn-xs">' +
                    '<span class="glyphicon glyphicon-remove"></span>' +
                  '</button>' +
                '</div>' +
              '</td>' +
              '<td class="td-right"><span class="amount">' + amount +'</span> g</td>' +
              '<td class="td-right"><span class="cals">' + cals +'</span> kcal</td>' +
            '</tr>';
            console.log(row);
  $('#' + meal).append(row);
}


// Fill food data on edit food modal
$(document).on("click", ".open-edit-food", function () {
  var id = $(this).data('food');
  var energy = $(this).data('energy');
  var name = $('#food-name-' + id).html();
  var carbo = $(this).data('carbo');
  var protein = $(this).data('protein');
  var fat = $(this).data('fat');
  $(".modal-body #edit-food-id").val(id);
  $(".modal-body #edit-food-name").val(name);
  $(".modal-body #edit-energy-amount").val(energy);
  $(".modal-body #edit-carbo-amount").val(carbo);
  $(".modal-body #edit-protein-amount").val(protein);
  $(".modal-body #edit-fat-amount").val(fat);
});




// Setup for handling csrf tokens in Django
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});

// Check state of add serving form and activate Add if fitting
function checkAddServingState() {
  var food_id = $('#food_id').val();
  var amount = $('#add_amount').val();
  if (food_id && amount) {
    $('#add_serving_submit').prop('disabled', false);
  } else {
    $('#add_serving_submit').prop('disabled', true);
  }
}


var protein_energy = 4;
var carbo_energy = 4;
var fat_energy = 9;

var protein_color = '#6ba8ed';
var carbo_color = '#97e165';
var fat_color = '#f0c943';

var pie_data = [];
var bar_data = [];

var pie_options = {
  series: {
    pie: {
      show: true,
      label: {
        show: true,
        radius: 1/2,
        formatter: function(label, series) { return Math.round(series.percent) + "%"; },
        background: {
          opacity: 0,
        },
      },
    },
  },
  legend: {
    show: false,
  },
};

var bar_options = {
  series: {
    bars: {
      show: true,
      barWidth: 0.75,
      align: 'center',
      fill: 1.0,
      lineWidth: 0,
      label: {
        show: true,
        formatter: function(label, series) { return Math.round(series); },
      }
    },
    lines: { show: false },
    points: { show: false },
  },
  xaxis: {
    show: true,
    mode: 'categories',
    tickLength: 0,
  },
  yaxis: {
    show: false,
    min: 0,
    max: 200,
  },
  legend: {
    show: false,
  },
  grid: {
    show: true,
    borderWidth: 0,
    margin: {
      top: 10,
      bottom: 10,
      right: 10,
      left: 10,
    },
  },
};

// Updates day and mealsubtotals
function updateDayInfo() {
  var url = document.URL + 'info/';
  $.get(url).done(function(data) {
    // Update total
    $('#cals').text(data.cals);

    // Update piechart (showing energy distribution)
    pie_data = [
      { data:[[1, data.fat * fat_energy]], color: fat_color },
      { data:[[2, data.protein * protein_energy]], color: protein_color },
      { data:[[3, data.carbo * carbo_energy]], color: carbo_color }
    ];
    $.plot('#macro-nutrients-piechart', pie_data, pie_options);

    // Update barchart (showing macro-amounts)
    bar_data = [
      { data:[[Math.round(data.protein), data.protein]], color: protein_color },
      { data:[[Math.round(data.carbo), data.carbo]], color: carbo_color },
      { data:[[Math.round(data.fat), data.fat]], color: fat_color }
    ];
    bar_options['yaxis']['max'] = Math.max(data.protein, data.carbo, data.fat) + 10;
    $.plot('#macro-nutrients-barchart', bar_data, bar_options);

    // Update nutrient-table
    $('#info-energy').text(Math.round(data.cals));
    $('#info-protein').text(Math.round(data.protein));
    $('#info-carbo').text(Math.round(data.carbo));
    $('#info-fat').text(Math.round(data.fat));

    // Update meal subtotals
    for(var prop in data.cals_by_meal) {
      $('#' + prop + '-cals').text(data.cals_by_meal[prop]);
      $('#' + prop + '-amount').text(data.amount_by_meal[prop]);
    }
  });
}

function updatePastebuffer() {
  var url = getBaseURL() + '/foodlog/paste/';
  $.get(url).done(function(data) {
    if (data.length === 0) {
      $('#pastebuffer-panel').hide();
      return;
    }
    $('#pastebuffer-panel').show();
    var content = "";
    for(var i = 0; i < data.length; i++) {
      pasterow = data[i];
      content = content + '<div data-pasterow="' + i + '"><span style="float: right">' + pasterow.amount + ' g</span>' + pasterow.name + '</div>';
    }
    $('#pastebuffer').html(content);
  });
}

$(function() {
  var div = $('#macro-nutrients-piechart');
  div.css('height', div.width());
  div = $('#macro-nutrients-barchart');
  div.css('height', div.width());

  var calendar = $('.datepicker').datepicker({
    format: "yyyy-mm-dd",
    weekStart: 1,
    todayHighlight: true
  });
  calendar.on('changeDate', function(e){
    window.location = '/foodlog/' + e.format();
  });
  calendar.datepicker('update', chosen_date);
  $('.datepicker-inline').addClass('center-block');

  updateDayInfo();
  updatePastebuffer();
});

function getBaseURL() {
  return window.location.protocol + '//' + window.location.host;
}









