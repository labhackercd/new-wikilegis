/*global $ events Urls prefixURL */

var ParticipantsAutocompleteView = function() {};

ParticipantsAutocompleteView.prototype.initEvents = function() {
  this.inputNameElement = $('.js-openParticipation .js-search-name');
  this.filter = $('.js-openParticipation .js-searchFilter');
  this.clearFiltersElement = $('.js-openParticipation .js-clearFilters');
  this.filterListElement = $('.js-openParticipation .js-filterList');
  this.filterBarElement = $('.js-openParticipation .js-filterBar');
  this.initAutocompleteInput();
  this.publishers();
  this.subscribers();
};

ParticipantsAutocompleteView.prototype.publishers = function() {
  $(window).keydown(function(event){
    if (event.keyCode == 13 && !$(event.target).hasClass('js-search-name')) {
      event.preventDefault();
      return false;
    }
  });
  $('.js-sendButton').click(function() {
    events.createInvitedGroup.publish();
  });
  $('.js-filterButton').click(function() {
    events.applyFilters.publish();
  });
  $('.js-selectedProfile').on('click', '.js-user', function(e) {
    var userId = $(e.target).closest('.js-user').data('userId').toString();
    events.removeParticipant.publish(userId);
  });
  $('.js-selectedProfile').on('click', '.js-email', function(e) {
    var email = $(e.target).closest('.js-email').data('email');
    events.removeEmail.publish(email);
  });
  $('.js-selectedProfile').bind('DOMSubtreeModified', function(){
    var countSelecteds = $('.js-selectedProfile').children().length;
    events.setCounterSelecteds.publish(countSelecteds);
  });
  this.filter.on('click', function() {
    events.openFilterModal.publish();
  });
  this.clearFiltersElement.on('click', function() {
    events.clearFilters.publish();
  });
};

ParticipantsAutocompleteView.prototype.subscribers = function () {
  var self = this;
  events.removeParticipant.subscribe(function(userId){
    self.removeParticipant(userId);
  });
  events.removeEmail.subscribe(function(email){
    self.removeEmail(email);
  });
  events.setCounterSelectables.subscribe(function(countSelectables){
    self.setCounterSelectables(countSelectables);
  });
  events.setCounterSelecteds.subscribe(function(countSelecteds){
    self.setCounterSelecteds(countSelecteds);
  });
  events.updateSearchParticipants.subscribe(function(){
    self.updateSearchParticipants();
  });
  events.clearFilters.subscribe(function(){
    self.clearFilters();
  });
  events.showFilters.subscribe(function(){
    self.showFilters();
  });
};

ParticipantsAutocompleteView.prototype.setCounterSelectables = function (countSelectables) {
  $('.js-countSelectables').text(countSelectables);
  if(countSelectables == 0) {
    $('.js-countSelectables').parent().parent().addClass('-empty');
  } else {
    $('.js-countSelectables').parent().parent().removeClass('-empty');
  }
};

ParticipantsAutocompleteView.prototype.setCounterSelecteds = function (countSelecteds) {
  $('.js-countSelecteds').text(countSelecteds);
  if(countSelecteds == 0) {
    $('.js-countSelecteds').parent().parent().addClass('-empty');
  } else {
    $('.js-countSelecteds').parent().parent().removeClass('-empty');
  }
};

ParticipantsAutocompleteView.prototype.removeParticipant = function (userId) {
  $('.js-selectedProfile .js-user[data-user-id='+ userId +']').remove();
  $('input[name="participants"][value="' + userId + '"]').remove();
};

ParticipantsAutocompleteView.prototype.removeEmail = function (email) {
  $('.js-selectedProfile .js-email[data-email="'+ email +'"]').remove();
  $('input[name="emails"][value="' + email + '"]').remove();
};


ParticipantsAutocompleteView.prototype.participantItem = function (add, user_id, first_name, last_name, avatar, themes) {
  var tags = '';
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
      <img class="avatar" src="${avatar || prefixURL ? prefixURL + '/static/img/avatar.png' : '/static/img/avatar.png'}">
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
  `;
  return element;
};

ParticipantsAutocompleteView.prototype.updateSearchParticipants = function () {
  var self = this;
  self.inputNameElement.autocomplete('search');
};

ParticipantsAutocompleteView.prototype.initAutocompleteInput= function () {
  var self = this;

  self.inputNameElement.autocomplete({
    source: function(request, response) {
      var theme = undefined;
      if (localStorage.getItem('theme')) {
        theme = localStorage.getItem('theme').split(',');
      }
      var group = undefined;
      if (localStorage.getItem('group')) {
        group = localStorage.getItem('group').split(',');
      }
      var minAge = undefined;
      if (localStorage.getItem('minAge')) {
        minAge = localStorage.getItem('minAge');
      }
      var maxAge = undefined;
      if (localStorage.getItem('maxAge')) {
        maxAge = localStorage.getItem('maxAge');
      }
      var gender = undefined;
      if (localStorage.getItem('gender')) {
        gender = localStorage.getItem('gender');
      }
      var locale = undefined;
      if (localStorage.getItem('locale')) {
        locale = localStorage.getItem('locale');
      }
      var participants = [];
      $('.js-selectedProfile .js-user').each(function() {
        participants.push($(this).data('userId'));
      });
      $.ajax({
        url: Urls.participants_autocomplete(),
        dataType: 'json',
        traditional: true,
        data: {
          name: request.term,
          theme: theme,
          group: group,
          minAge: minAge,
          maxAge: maxAge,
          gender: gender,
          locale: locale,
          selected_participants: participants
        },
        success: function(data) {
          events.setCounterSelectables.publish(data.length);
          response(data);
        }
      });
    },
    minLength: 0,
    appendTo: '.js-inputProfile',
    messages: {
      noResults: '',
      results: function() {}
    },
    open: function() {
      $('.ui-autocomplete').css('position', 'relative');
      $('.ui-autocomplete').css('top', '0px');
      $('.ui-autocomplete').css('left', '0px');
    },
    select: function(event, ui) {
      self.addParticipant(ui.item.id);
      var element = self.participantItem(false, ui.item.id, ui.item.first_name, ui.item.last_name, ui.item.avatar, ui.item.themes);
      $(element).prependTo('.js-selectedProfile');
      $('.js-selectedProfile').scrollTop(0);
      $(this).autocomplete('search');
      $(`.js-inputProfile .js-user[data-user-id=${ui.item.id}]`).hide();
    }
  })
    .bind('keypress', function(){
      $(this).autocomplete('search');
    })
    .data('ui-autocomplete')._renderItem = function (ul, item) {
      var element = self.participantItem(true, item.id, item.first_name, item.last_name, item.avatar, item.themes);
      return $(element).appendTo(ul);
    };

  self.inputNameElement.keypress(function (e) {
    if (e.which == 13) {
      var email = self.inputNameElement.val();
      if (self.validateEmail(email)) {
        var element = `
        <div class="user-profile js-email" data-email="${email}">
          <img class="avatar" src="${prefixURL ? prefixURL + '/static/img/avatar.png' : '/static/img/avatar.png'}">
          <div class="info">
            <span class="name">${email}</span>
          </div>
          <div class="action">
            <div class="remove"></div>
          </div>
        </div>
        `;
        $(element).prependTo('.js-selectedProfile');
        self.inputNameElement.val('');
        self.addEmail(email);
      }
      return false;
    }
  });
};

ParticipantsAutocompleteView.prototype.validateEmail = function (email) {
  var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
};

ParticipantsAutocompleteView.prototype.addParticipant = function(participantId) {
  var participantInput = $('input[name="participants"][value="' + participantId + '"]');
  if (participantInput.length === 0) {
    var input = $('<input type="hidden" name="participants" value="' + participantId + '">');
    $('.js-participants').append(input);
  }
};

ParticipantsAutocompleteView.prototype.addEmail = function(email) {
  var emailInput = $('input[name="emails"][value="' + email + '"]');
  if (emailInput.length === 0) {
    var input = $('<input type="hidden" name="emails" value="' + email + '">');
    $('.js-participants').append(input);
  }
};

ParticipantsAutocompleteView.prototype.clearFilters = function () {
  var self = this;
  localStorage.clear();
  events.resetFilterModalForm.publish();
  events.updateSearchParticipants.publish();
  self.filterListElement.html('');
  self.filterBarElement.addClass('_hidden');
};

ParticipantsAutocompleteView.prototype.showFilters = function () {
  var self = this;

  self.filterBarElement.removeClass('_hidden');

  if(localStorage.getItem('theme')){
    $('.js-tag').each(function(){
      self.filterListElement.append(`
        <li class="item">${$(this).text()}</li>
      `);
    });
  }
  if(localStorage.getItem('minAge')){
    self.filterListElement.append(`
      <li class="item">${$('.js-minAge').val()}</li>
    `);
  }
  if(localStorage.getItem('maxAge')){
    self.filterListElement.append(`
      <li class="item">${$('.js-maxAge').val()}</li>
    `);
  }
  if(localStorage.getItem('gender')){
    self.filterListElement.append(`
      <li class="item">${$('.js-gender option:selected').text()}</li>
    `);
  }
  if(localStorage.getItem('locale')){
    self.filterListElement.append(`
      <li class="item">${$('.js-locale option:selected').text()}</li>
    `);
  }

};
