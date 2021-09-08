/*global $ events */

var ConfirmFormModalView = function() {};

ConfirmFormModalView.prototype.initEvents = function() {
  this.confirmFormModalElement = $('.js-confirmFormModal');
  this.openConfirmFormButton = $('.js-openConfirmFormButton');
  this.closeElements = $('.js-confirmFormModal .js-close');
  this.subscribers();
  this.publishers();
};

ConfirmFormModalView.prototype.subscribers = function () {
  var self = this;
  events.openConfirmFormModal.subscribe(function() {
    self.confirmFormModalElement.addClass('-show');
  });
  events.closeConfirmFormModal.subscribe(function() {
    self.confirmFormModalElement.removeClass('-show');
  });
};

ConfirmFormModalView.prototype.publishers = function () {
  var self = this;

  self.openConfirmFormButton.on('click', function() {
    events.openConfirmFormModal.publish();
  });

  self.closeElements.on('click', function() {
    events.closeConfirmFormModal.publish();
  });
};