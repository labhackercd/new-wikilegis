/*global $ events Urls */

var SuggestionInputController = function() {};

SuggestionInputController.prototype.initEvents = function() {
  this.subscribers();
};

SuggestionInputController.prototype.subscribers = function() {
  var self = this;

  $.Topic(events.sendSuggestion).subscribe(function(excerptId, selectedText, suggestion) {
    self.sendSuggestion(excerptId, selectedText, suggestion);
  });
};

SuggestionInputController.prototype.sendSuggestion = function(excerptId, startSelection, endSelection, suggestion) {
  var request = $.ajax({
    url: Urls.new_suggestion(),
    method: 'POST',
    data: {
      excerptId: excerptId,
      startSelection: startSelection,
      endSelection: endSelection,
      suggestion: suggestion
    }
  })

  request.done(function(data) {
    $.Topic(events.suggestionCreated).publish(data.id, data.html);
  })

  request.fail(function(jqXHR) {
    $.Topic(events.showSuggestionInputError).publish(jqXHR.responseJSON.error);
  })
};