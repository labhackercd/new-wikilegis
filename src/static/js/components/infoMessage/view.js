/*global $ events */

var InfoMessageView = function() {};

InfoMessageView.prototype.initEvents = function() {
  this.infoMessageElement = $('.js-infoMessage');
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
    setTimeout(events.closeInfoMessage.publish, 4000)
  });
};

InfoMessageView.prototype.hide = function () {
  this.infoMessageElement.hide();
};
