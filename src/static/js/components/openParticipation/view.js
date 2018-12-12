/*global $ events Urls */

var ParticipantsAutocompleteView = function() {};

ParticipantsAutocompleteView.prototype.initEvents = function() {
  this.inputNameElement = $('.js-name');
  this.initAutocompleteInput();
  this.publishers();
  this.subscribers();
};

ParticipantsAutocompleteView.prototype.publishers = function() {
  var self = this;
  $('.js-send-button').click(function() {
    $.Topic(events.createInvitedGroup).publish();
  });
  $('.js-theme').click(function(e) {
    var themeId = $(e.target).data('themeId').toString();
    $.Topic(events.setThemes).publish(themeId);
  });
};

ParticipantsAutocompleteView.prototype.subscribers = function () {
  var self = this;
  $.Topic(events.setThemes).subscribe(function(themeId){
    self.setThemes(themeId);
  });
};


ParticipantsAutocompleteView.prototype.setThemes = function (themeId) {
  var self = this;
  var currentValue = localStorage.getItem('theme');
  var key = 'theme';

  if (currentValue) {
    var currentArray = currentValue.split(',');
    var i = currentArray.indexOf(themeId);
    if (i < 0) {
      currentArray = currentArray.concat(themeId);
      localStorage.setItem(key, currentArray);
      self.inputNameElement.focus();
    } else {
      currentArray.splice(i, 1);
      if (currentArray.length > 0) {
        localStorage.setItem(key, currentArray);
        self.inputNameElement.focus();
      } else {
        localStorage.removeItem(key);
      }
    }
  } else {
    localStorage.setItem(key, themeId);
    self.inputNameElement.focus();
  }

  $(window).on('unload', function() {
    localStorage.clear();
  });
};

ParticipantsAutocompleteView.prototype.initAutocompleteInput= function () {
  var self = this;

  self.inputNameElement.autocomplete({
    source: function(request, response) {
      var theme = undefined;
      if (localStorage.getItem('theme')) {
        theme = localStorage.getItem('theme').split(',');
      }
      $.ajax({
        url: Urls.participants_autocomplete(),
        dataType: 'json',
        traditional: true,
        data: {
          name: request.term,
          theme: theme
        },
        success: function(data) {
          response(data);
        }
      });
    },
    minLength: 0,
    select: function(event, ui) {
      $('<div>').text(ui.item.first_name)
        .addClass('js-user')
        .attr('data-user-id', ui.item.id)
        .prependTo('#log');
      $('#log').scrollTop(0);
    }
  })
    .bind('focus', function(){ $(this).autocomplete('search');})
    .data('ui-autocomplete')._renderItem = self.listItem;


  self.inputNameElement.keypress(function (e) {
    if (e.which == 13) {
      var email = self.inputNameElement.val();
      if (self.validateEmail(email)) {
        $('<div>').text(email)
          .addClass('js-email')
          .attr('data-email', email)
          .prependTo('#log');
        $('#log').scrollTop(0);
        self.inputNameElement.val('');
      }
      return false;
    }
  });
};

ParticipantsAutocompleteView.prototype.listItem = function (ul, item) {
  return $('<li>').append('<a>' + item.first_name + '</a>').appendTo(ul);
};

ParticipantsAutocompleteView.prototype.validateEmail = function (email) {
  var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
};