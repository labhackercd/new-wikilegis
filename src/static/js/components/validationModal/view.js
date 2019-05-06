/*global $ events */

var ValidationModalView = function() {};

ValidationModalView.prototype.initEvents = function() {
  this.validationModalElement = $('.js-validateModal');
  this.openValidationButton = $('.js-openValidationButton');
  this.closeElements = $('.js-validateModal .js-close');
  this.subscribers();
  this.publishers();
};

ValidationModalView.prototype.subscribers = function () {
  var self = this;
  events.openValidationModal.subscribe(function() {
    self.validationModalElement.addClass('-show');
  });
  events.closeValidationModal.subscribe(function() {
    self.validationModalElement.removeClass('-show');
  });
};

ValidationModalView.prototype.publishers = function () {
  var self = this;

  self.openValidationButton.on('click', function() {
    events.openValidationModal.publish();
  });

  self.closeElements.on('click', function() {
    events.closeValidationModal.publish();
  });
};