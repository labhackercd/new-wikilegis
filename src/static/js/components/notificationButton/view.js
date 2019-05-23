/*global $ events */

var NotificationButtonView = function() {};

NotificationButtonView.prototype.initEvents = function() {
  this.notificationButtonElement = $('.js-notificationButton');
  this.notificationListElement = $('.js-notificationList');

  this.subscribers();
  this.publishers();
};

NotificationButtonView.prototype.subscribers = function () {
  var self = this;

  events.closeNotificationList.subscribe(function() {
    self.notificationButtonElement.parent().removeClass('-active');
    self.notificationListElement.children().removeClass('-new');
  });
};

NotificationButtonView.prototype.publishers = function () {
  var self = this;

  self.notificationButtonElement.on('click', function() {
    $(this).parent().toggleClass('-active');
    $(this).parent().removeClass('-notified');
    events.updateNotifications.publish();
  });
};

