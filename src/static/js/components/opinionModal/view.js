/*global $ events */

var OpinionModalView = function() {};

OpinionModalView.prototype.initEvents = function() {
  this.userInfoElement = $('.js-opinionModal .js-userInfo');
  this.userAvatarElement = $('.js-opinionModal .js-userAvatar');
  this.userNameElement = $('.js-opinionModal .js-userName');
  this.documentExcerptElement = $('.js-opinionModal .js-documentExcerpt');
  this.suggestionElement = $('.js-opinionModal .js-suggestion');

  this.publishers();
  this.subscribers();
};

OpinionModalView.prototype.publishers = function() {
  $('.js-closeModal').click(function() {
    $.Topic(events.closeOpinionModal).publish();
  });

  $(document).ready(function(){
    if ($('.js-opinionModal').data('openOnLoad') === true) {
      $.Topic(events.openOpinionModal).publish(null);
    }
  });
};

OpinionModalView.prototype.subscribers = function () {
  var self = this;

  $.Topic(events.openOpinionModal).subscribe(function(){
    self.show();
  });

  $.Topic(events.closeOpinionModal).subscribe(function(){
    self.hide();
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