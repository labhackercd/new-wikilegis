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
  var request = $.ajax({
    url: Urls.document_text(documentId),
    method: 'GET',
  });

  request.done(function(data) {
    if (data.html.trim() !== '') {
      events.documentTextLoaded.publish(data.html);
    }
  });

};