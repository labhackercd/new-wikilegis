/*global $ events Urls */

var OpinionModalController = function() {};

OpinionModalController.prototype.initEvents = function() {
  this.subscribers();
};

OpinionModalController.prototype.subscribers = function() {
  var self = this;

  $.Topic(events.openOpinionModal).subscribe(function(excerptId) {
    self.getRandomSuggestion(excerptId);
  });

  $.Topic(events.sendOpinion).subscribe(function(suggestionId, opinion) {
    self.sendOpinion(suggestionId, opinion);
  });
};

OpinionModalController.prototype.getRandomSuggestion = function(excerptId) {
  var regex = /\/p\/(\d+)-.*/g;
  var match = regex.exec(document.location.pathname);
  var data = {
    documentId: match[1],
    excerptId: excerptId
  };

  var request = $.ajax({
    url: Urls.get_random_suggestion(),
    method: 'POST',
    data: data
  });

  request.done(function(data) {
    $.Topic(events.fillOpinionModal).publish(data.user, data.excerpt, data.suggestion);
  });

  request.fail(function() {
    $.Topic(events.closeOpinionModal).publish(false);
  });
};

OpinionModalController.prototype.sendOpinion = function(suggestionId, opinion) {
  var request = $.ajax({
    url: Urls.new_opinion(),
    method: 'POST',
    data: {
      suggestionId: suggestionId,
      opinion: opinion
    }
  });

  request.done(function() {
    $.Topic(events.closeOpinionModal).publish(true);
  });
};