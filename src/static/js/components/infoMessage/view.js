/*global $ events */

var InfoMessageView = function() {};

InfoMessageView.prototype.initEvents = function() {
  this.infoMessageElement = $('.js-infoMessage');
  this.closeMessage = $('.js-closeMessage');
  this.subscribers();
  this.publishers();
};

InfoMessageView.prototype.subscribers = function () {
  var self = this;
  events.closeInfoMessage.subscribe(function(){
    self.hide();
  });
};

InfoMessageView.prototype.publishers = function () {
  var self = this;
  $(window).on('load', function() {
    self.infoMessageElement.addClass('-show');
    setTimeout(events.closeInfoMessage.publish, 4000);
  });
  self.closeMessage.on('click', function() {
    events.closeInfoMessage.publish();
  });
};

InfoMessageView.prototype.hide = function () {
  this.infoMessageElement.removeClass('-show');
};
