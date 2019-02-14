/*global $ events */

var AlertMessageController = function() {};

AlertMessageController.prototype.initEvents = function() {
  this.subscribers();
}

AlertMessageController.prototype.subscribers = function() {
  var self = this;
  events.activateAlertAction.subscribe(function(actionUrl) {
    self.sendAction(actionUrl);
  })
};

AlertMessageController.prototype.sendAction = function(actionUrl) {
  var request = $.ajax({
    url: actionUrl,
    method: 'POST'
  });

  request.done(function(data) {
    events.stopAlertProgress.publish(true);
    if (data.action === 'undo') {
      events.suggestionUndone.publish(data.suggestion);
    }
  });
};