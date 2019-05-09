/*global $ events */

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

ToolBarController.prototype.saveDocumentData = function(data) {
  console.log(data);
  var request = $.ajax({
    url: Urls.save_document(data.pk),
    method: 'POST',
    data: data
  });

  request.done(function(data) {
    events.showMessage.publish(data.message, 'success', null);
  });

  request.fail(function(jqXHR) {
    events.showSuggestionInputError.publish(jqXHR.responseJSON.error);
  });
};