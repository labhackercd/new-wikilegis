/*global $ events Urls */

var FeedbackFormController = function() {};

FeedbackFormController.prototype.initEvents = function() {
  this.subscribers();
};

FeedbackFormController.prototype.subscribers = function() {
  var self = this;

  events.openFeedbackFormModal.subscribe(function() {
    self.populateNamedVersions();
  });
};

FeedbackFormController.prototype.populateNamedVersions = function() {
  var documentId = $('.js-documentEditor').data('documentId');
  var request = $.ajax({
    url: Urls.list_document_versions(documentId),
    method: 'GET',
  });

  request.done(function(data) {
    var versionList = $('.js-feedbackFormModal .js-versionsSelect');
    versionList.html('');
    $.each(data.versions, function(idx, value) {
      versionList.append(`<option value="${value.pk}">${value.name}</option>`);
    });
    versionList.parent().addClass('-filled');
  });
};