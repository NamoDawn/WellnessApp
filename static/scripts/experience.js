const $ = window.$;

$(document).ready(function () {
  let stagedExp = [];
  let stagedObj = [];
  let userId;

  userId = JSON.parse(atob(localStorage.getItem('data')))['user_id'];
  /* launches data visualization */
  $('#show_button').on('click', function() {
    showVisualization(userId);
  });


  /* Positive Experience Button Clicked adds to build stagedObj */
  $('#positive-add').on('click', function () {
    const name = $('#positive').val();
    let scale = $('#positive_scale').val();

    queueExp(name, scale, 'positive');
    $('#positive').val('');
    $('#positive_scale').val('');
  });
  /* saves staged data to 'experiences' table */
  $('#stow_button').on('click', function () {
    saveExperiences(stagedObj);
    $('#experienceAdded').empty();
    stagedExp = [];
    stagedObj = [];
  });
  /* Negative Experience Button Clicked adds to build stagedObj */
  $('#negative-add').click(function () {
    let name = $('#negative').val();
    let scale = $('#negative_scale').val();

    queueExp(name, scale, 'negative');
    $('#negative').val('');
    $('#negative_scale').val('');
  });
  /* 'Remove' icon clicked
   * deletes stagedObj that was clicked */
  $('body').on('click', '.remove-icon', function () {
    /* delete the element */
    $(this).parent().fadeOut(300);
    let index = stagedExp.indexOf($(this).children().attr('exp_name'));
    stagedExp.splice(index, 1);
    /* update the stagedObj */
    for (let i = 0; i < stagedObj.length; i++) {
      if (stagedObj[i].name === $(this).children().attr('exp_name')) {
        stagedObj.splice(i, 1);
      }
    }
  });
  /* Adds the experience to the DOM as an icon/string in preparation for DB stow */
  function queueExp (name, scale, type) {
    if (scale === '') {
      scale = 5;
    }
    if (!stagedExp.includes(name) && name !== '') {
      const experienceadded = $('#experienceAdded');
      let grid = $('<div/>', {class: 'col-xs-3'}).appendTo(experienceadded);
      const icon = $('<span/>', {class: 'glyphicon glyphicon-remove-circle remove-icon'}).appendTo(grid);
      const text = $('<span/>', {class: 'symdisplay', id: name + scale, name: name, text: name + '(' + scale + ')'}).appendTo(icon);
      stagedExp.push(name);
      stagedObj.push({'exp_name': name, 'scale': scale, 'type': type, 'user_id': userId});
    }
  }
  /* Writes staged experiences to 'experiences' table */
  function saveExperiences (stagedObj) {
    $.ajax({
      async: false,
      url: '/save_exp',
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify(stagedObj),
      success: function (res) {
        return res;
      },
      error: function (res) {
        console.error('Error: ' + res);
      }
    });
  }
  /* Fetches experiences based on date rage and user id */
  function showVisualization (userId) {
    $.ajax({
      url: '/vis',
      type: 'POST',
      contentType: 'text/csv',
      data: JSON.stringify(userId),
      success: function (res) {
	  $(location).attr('href', 'http://54.193.75.123/load_vis');
      },
      error: function (error) {
        console.error('Error: ' + error);
      }
    });
  }
});
