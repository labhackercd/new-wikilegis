/*global $ events Urls */

var ToolBarController = function() {};

ToolBarController.prototype.initEvents = function() {
  this.subscribers();
  this.publishers();
};


ToolBarController.prototype.subscribers = function() {
  var self = this;

  events.saveDocument.subscribe(function(data) {
    self.saveDocumentData(data);
  });
};

ToolBarController.prototype.publishers = function() {
};

ToolBarController.prototype.saveDocumentData = function(updateData) {
  var request = $.ajax({
    url: Urls.save_document(updateData.pk),
    method: 'POST',
    data: updateData
  });

  request.done(function(data) {
    if (!updateData.autoSave) {
      events.showMessage.publish(data.message, 'success', null);
    }
    events.documentSaved.publish(data);
  });

  request.fail(function(jqXHR) {
    events.showSuggestionInputError.publish(jqXHR.responseJSON.error);
  });
};