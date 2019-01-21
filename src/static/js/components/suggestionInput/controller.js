/*global $ events Urls */

var SuggestionInputController = function() {};

SuggestionInputController.prototype.initEvents = function() {
  this.subscribers();
};

SuggestionInputController.prototype.subscribers = function() {
  var self = this;

  events.sendSuggestion.subscribe(function(groupId, excerptId, startSelection, endSelection, suggestion) {
    self.sendSuggestion(groupId, excerptId, startSelection, endSelection, suggestion);
  });
};

SuggestionInputController.prototype.sendSuggestion = function(groupId, excerptId, startSelection, endSelection, suggestion) {
  var request = $.ajax({
    url: Urls.new_suggestion(groupId),
    method: 'POST',
    data: {
      excerptId: excerptId,
      startSelection: startSelection,
      endSelection: endSelection,
      suggestion: suggestion
    }
  });

  request.done(function(data) {
    events.suggestionCreated.publish(data.id, data.html);
  });

  request.fail(function(jqXHR) {
    events.showSuggestionInputError.publish(jqXHR.responseJSON.error);
  });
};
