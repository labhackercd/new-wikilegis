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
    console.log(data);
    events.stopAlertProgress.publish(true);
  });
};