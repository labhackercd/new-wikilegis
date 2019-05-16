/*global $ events autosize */

var DocumentEditorController = function() {};

DocumentEditorController.prototype.initEvents = function() {
  this.publishers();
};

DocumentEditorController.prototype.publishers = function() {
  var self = this;
  self.loadTextData();
};

DocumentEditorController.prototype.loadTextData = function() {
  var documentId = $('.js-documentEditor').data('documentId');

  var searchParams = new URLSearchParams(window.location.search);
  var currentVersion = ''
  if (searchParams.has('version')) {
    currentVersion = searchParams.get('version');
  }

  var request = $.ajax({
    url: Urls.document_text(documentId) + '?version=' + currentVersion,
    method: 'GET',
  });

  request.done(function(data) {
    if (data.html.trim() !== '') {
      events.documentTextLoaded.publish(data.html);
    }
  });

  request.fail(function(jqXHR) {
    var data = jqXHR.responseJSON;
    events.showMessage.publish(data.message, 'fail', null);

    if (data.html.trim() !== '') {
      events.documentTextLoaded.publish(data.html);
    }
  })
};