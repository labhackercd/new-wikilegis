/*global $ events Urls */

var ParticipantsAutocompleteView = function() {};

ParticipantsAutocompleteView.prototype.initEvents = function() {
  this.inputNameElement = $('.js-search-name');
  this.initAutocompleteInput();
  this.publishers();
  this.subscribers();
};

ParticipantsAutocompleteView.prototype.publishers = function() {
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

ParticipantsAutocompleteView.prototype.participantItem = function (add, user_id, first_name, last_name, avatar, themes) {
  var tags = ''
  for(var index in themes){
    tags = tags.concat(`
      <div class="theme-tag">
        <span class="dot" style="background-color: ${themes[index].color};"></span>
         ${themes[index].name}
      </div>
      `);
  }
  var element = `
    <div class="user-profile js-user" data-user-id="${user_id}">
      <img class="avatar" src="${avatar || '/static/img/avatar.png'}">
      <div class="info">
        <span class="name">${first_name} ${last_name}</span>
        <div class="tags">
          ${tags}
        </div>
      </div>
      <div class="action">
        <div class="${add ? 'add' : 'remove'}"></div>
      </div>
    </div>
  `
  return element;
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
    appendTo: '.js-inputProfile',
    open: function(event, ui) {
      $(".ui-autocomplete").css("position", "relative");
      $(".ui-autocomplete").css("top", "0px");
      $(".ui-autocomplete").css("left", "0px");
    },
    select: function(event, ui) {
      var element = self.participantItem(false, ui.item.id, ui.item.first_name, ui.item.last_name, ui.item.avatar, ui.item.themes);
      $(element).prependTo('.js-selectedProfile');
      $('.js-selectedProfile').scrollTop(0);
    }
  })
    .bind('focus', function(){ $(this).autocomplete('search');})
    .data('ui-autocomplete')._renderItem = function (ul, item) {
      var element = self.participantItem(true, item.id, item.first_name, item.last_name, item.avatar, item.themes);
      return $(element).appendTo(ul);
    };

  self.inputNameElement.keypress(function (e) {
    if (e.which == 13) {
      var email = self.inputNameElement.val();
      if (self.validateEmail(email)) {
        $('<div>').text(email)
          .addClass('js-email')
          .attr('data-email', email)
          .prependTo('.js-selectedProfile');
        self.inputNameElement.val('');
      }
      return false;
    }
  });
};

ParticipantsAutocompleteView.prototype.validateEmail = function (email) {
  var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
};
