/* global $ events */

var FeedbackFormModalView = function() {};

FeedbackFormModalView.prototype.initEvents = function () {
  this.feedbackFormModalElement = $('.js-feedbackFormModal');
  this.feedbackInfoModalElement = $('.js-feedbackInfoModal');
  this.feedbackWaitingModalElement = $('.js-feedbackWaitingModal');
  this.openFeedbackFormButton = $('.js-openFeedback');
  this.openFeedbackButton = $('.js-feedbackButton');
  this.closeFormElement = $('.js-feedbackFormModal .js-close');
  this.closeInfoElement = $('.js-feedbackInfoModal .js-close');
  this.closeWaitingElement = $('.js-feedbackWaitingModal .js-close');
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
  events.openFeedbackWaitingModal.subscribe(function () {
    self.feedbackWaitingModalElement.addClass('-show');
  });
  events.closeFeedbackWaitingModal.subscribe(function () {
    self.feedbackWaitingModalElement.removeClass('-show');
  });
};

FeedbackFormModalView.prototype.publishers = function () {
  var self = this;

  self.openFeedbackFormButton.on('click', function (e) {
    e.preventDefault();
    events.closeFeedbackInfoModal.publish();
    events.openFeedbackFormModal.publish();
  });

  self.closeFormElement.on('click', function() {
    events.feedbackFormModalElement.publish();
  });

  self.openFeedbackButton.on('click', function (e) {
    e.preventDefault();
    if ($(e.target).closest('.js-feedbackButton').hasClass('-waiting')) {
      events.openFeedbackWaitingModal.publish();
    } else {
      events.openFeedbackInfoModal.publish();
    }
  });

  self.closeInfoElement.on('click', function() {
    events.closeFeedbackInfoModal.publish();
  });

  self.closeWaitingElement.on('click', function () {
    events.closeFeedbackWaitingModal.publish();
  });

  $('.js-feedbackFormModal .js-send').on('click', function (e) {
    e.preventDefault();
    self.sendFeedbackForm();
  });

};

FeedbackFormModalView.prototype.sendFeedbackForm = function () {
  var groupId = $('.js-feedbackFormModal').data('groupId');
  var youtubeId = $('.js-feedbackFormModal .js-youtubeId').val();
  var finalVersion = $('.js-feedbackFormModal .js-versionsSelect').val();

  events.sendFeedbackForm.publish(
    groupId,
    youtubeId,
    finalVersion
  );
};
