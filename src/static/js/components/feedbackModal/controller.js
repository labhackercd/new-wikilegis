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

  events.sendFeedbackForm.subscribe(function (
    groupId, youtubeUrl, finalVersion) {
    self.sendFeedbackForm(groupId, youtubeUrl, finalVersion);
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

FeedbackFormController.prototype.sendFeedbackForm = function (
  groupId, youtubeUrl, finalVersion) {
  var request = $.ajax({
    url: Urls.set_final_version(groupId),
    method: 'POST',
    data: {
      version_id: finalVersion,
      youtube_url: youtubeUrl
    }
  });

  request.done(function () {
    events.closeFeedbackFormModal.publish();
    $('.js-feedbackButton').addClass('-waiting');
  });

  request.fail(function (jqXHR) {
    $('.js-formError').html(`
        <li>${jqXHR.responseJSON.error}</li>
    `);
  });

};