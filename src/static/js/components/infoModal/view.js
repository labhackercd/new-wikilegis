/*global $ events */

var InfoModalView = function() {};

InfoModalView.prototype.initEvents = function() {
  this.infoModalElement = $('.js-infoModal');
  this.subscribers();
};

InfoModalView.prototype.subscribers = function () {
  var self = this;
  events.openInfoModal.subscribe(function() {
    self.infoModalElement.addClass('-show');
  });
};
