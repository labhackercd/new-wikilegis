/*global $ events */

var OpinionModalController = function() {};

OpinionModalController.prototype.initEvents = function() {
  this.subscribers();
};

OpinionModalController.prototype.subscribers = function() {
  var self = this;

  $.Topic(events.openOpinionModal).subscribe(function(excerptId) {
    self.getRandomSuggestion(excerptId);
  });
};

OpinionModalController.prototype.getRandomSuggestion = function(excerptId) {
  var regex = /\/p\/(\d+)-.*/g;
  var match = regex.exec(document.location.pathname);
  data = {
    documentId: match[1],
    excerptId: excerptId
  }

  var request = $.ajax({
    url: Urls.get_random_suggestion(),
    method: 'POST',
    data: data
  });

  request.done(function(data) {
    $.Topic(events.fillOpinionModal).publish(data.user, data.excerpt, data.suggestion);
  });
};