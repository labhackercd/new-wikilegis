/*global $ events Urls */

var DocumentEditorController = function() {};

DocumentEditorController.prototype.initEvents = function() {
  this.subscribers();
  this.publishers();
};

DocumentEditorController.prototype.subscribers = function() {
  var self = this;

  events.loadDocumentText.subscribe(function() {
    self.loadTextData();
  });
};

DocumentEditorController.prototype.publishers = function() {
  events.loadDocumentText.publish();
};

DocumentEditorController.prototype.loadTextData = function() {
  var documentId = $('.js-documentEditor').data('documentId');

  var searchParams = new URLSearchParams(window.location.search);
  var currentVersion = '';
  if (searchParams.has('version')) {
    currentVersion = searchParams.get('version');
  }

  var request = $.ajax({
    url: Urls.document_text(documentId) + '?version=' + currentVersion,
    method: 'GET',
  });

  request.done(function(data) {
    if (data.html.trim() !== '') {
      events.documentTextLoaded.publish(data);
    }
  });

  request.fail(function(jqXHR) {
    var data = jqXHR.responseJSON;
    events.showMessage.publish(data.message, 'fail', null);

    if (data.html.trim() !== '') {
      events.documentTextLoaded.publish(data);
    }
  });
};