/*global $ events Urls */

var OpinionModalController = function() {};

OpinionModalController.prototype.initEvents = function() {
  this.subscribers();
};

OpinionModalController.prototype.subscribers = function() {
  var self = this;

  events.sendOpinion.subscribe(function(suggestionId, opinion) {
    self.sendOpinion(suggestionId, opinion);
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
    events.nextOpinion.publish();
  });
};
