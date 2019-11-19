/*global $ events */

var FeedbackFormModalView = function() {};

FeedbackFormModalView.prototype.initEvents = function () {
  this.feedbackFormModalElement = $('.js-feedbackFormModal');
  this.feedbackInfoModalElement = $('.js-feedbackInfoModal');
  this.openfeedbackFormButton = $('.js-openFeedback');
  this.closeFormElement = $('.js-feedbackFormModal .js-close');
  this.closeInfoElement = $('.js-feedbackInfoModal .js-close');
  this.subscribers();
  this.publishers();
};

FeedbackFormModalView.prototype.subscribers = function () {
  var self = this;
  events.openFeedbackFormModal.subscribe(function() {
    self.feedbackFormModalElement.addClass('-show');
  });
  events.closeFeedbackFormModal.subscribe(function() {
    self.feedbackFormModalElement.removeClass('-show');
  });
  events.openFeedbackInfoModal.subscribe(function() {
    self.feedbackInfoModalElement.addClass('-show');
  });
  events.closeFeedbackInfoModal.subscribe(function () {
    self.feedbackInfoModalElement.removeClass('-show');
  });
};

FeedbackFormModalView.prototype.publishers = function () {
  var self = this;

  self.openfeedbackFormButton.on('click', function (e) {
    e.preventDefault();
    events.openFeedbackFormModal.publish();
  });

  self.closeFormElement.on('click', function() {
    events.feedbackFormModalElement.publish();
  });

  self.closeInfoElement.on('click', function() {
    events.closeFeedbackInfoModal.publish();
  });

};