/*global $ events */

var OpinionModalView = function() {};

OpinionModalView.prototype.initEvents = function() {
  this.userInfoElement = $('.js-opinionModal .js-userInfo');
  this.userAvatarElement = $('.js-opinionModal .js-userAvatar');
  this.userNameElement = $('.js-opinionModal .js-userName');
  this.documentExcerptElement = $('.js-opinionModal .js-documentExcerpt');
  this.suggestionElement = $('.js-opinionModal .js-suggestion');
  this.buttonsElements = $('.js-opinionModal .js-opinionButton')
  this.documentSuggestion = undefined;
  this.currentExcerptId = undefined;

  this.publishers();
  this.subscribers();
};

OpinionModalView.prototype.publishers = function() {
  var self = this;
  $('.js-closeModal').click(function() {
    $.Topic(events.closeOpinionModal).publish(false);
  });

  $(document).ready(function(){
    if ($('.js-opinionModal').data('openOnLoad') === true) {
      self.documentSuggestion = true;
      $.Topic(events.openOpinionModal).publish(null);
    }
  });

  self.buttonsElements.on('click', function(){
    var button = $(this);
    $.Topic(events.sendOpinion).publish(
      self.suggestionElement.data('suggestionId'),
      button.data('opinion')
    );
  });
};

OpinionModalView.prototype.subscribers = function () {
  var self = this;

  $.Topic(events.openOpinionModal).subscribe(function(){
    self.show();
  });

  $.Topic(events.closeOpinionModal).subscribe(function(reopen){
    self.hide();
    if (reopen) {
      if (self.documentSuggestion) {
        $.Topic(events.openOpinionModal).publish(null);
      } else {
        $.Topic(events.openOpinionModal).publish(self.currentExcerptId);
      }
    } else {
      self.documentSuggestion = undefined;
      self.currentExcerptId = undefined;
    }
  });

  $.Topic(events.fillOpinionModal).subscribe(function(user, excerpt, suggestion) {
    self.fill(user, excerpt, suggestion);
  })
};

OpinionModalView.prototype.hide = function () {
  $('.js-opinionModal').removeClass('-show');
};

OpinionModalView.prototype.show = function () {
  $('.js-opinionModal').addClass('-show');
};

OpinionModalView.prototype.fill = function(user, excerpt, suggestion) {
  var self = this;

  self.userAvatarElement.attr('src', user.avatar);
  self.userNameElement.text(user.fullName);
  self.userInfoElement.data('userId', user.id);
  self.documentExcerptElement.html(excerpt.html);
  self.documentExcerptElement.data('excerptId', excerpt.id);
  self.suggestionElement.text(suggestion.text)
  self.suggestionElement.data('suggestionId', suggestion.id);
};