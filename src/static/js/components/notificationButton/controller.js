/*global $ events Urls */

var NotificationController = function() {};

NotificationController.prototype.initEvents = function() {
  this.subscribers();
};


NotificationController.prototype.subscribers = function() {
  var self = this;

  events.updateNotifications.subscribe(function() {
    self.readNotifications();
  });
};

NotificationController.prototype.readNotifications = function() {
  $.ajax({
    url: Urls.read_notifications(),
    method: 'POST'
  });
};