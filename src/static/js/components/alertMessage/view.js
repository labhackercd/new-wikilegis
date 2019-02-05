/*global $ events */

var AlertMessageView = function() {};

AlertMessageView.prototype.initEvents = function () {
  this.alertMessageElement = $('.js-alertMessage');
  this.actionsElement = $('.js-alertMessage .js-actions');
  this.messageElement = $('.js-alertMessage .js-message');
  this.progressElement = $('.js-alertMessage .js-progress');

  this.subscribers();
  this.publishers();
};

AlertMessageView.prototype.subscribers = function () {
  var self = this;
  events.showMessage.subscribe(function (message, messageType, undo) {
    if (messageType != 'success' && messageType != 'fail') {
      messageType = 'default';
    }
    self.show(message, messageType, undo);
  });
};

AlertMessageView.prototype.publishers = function () {

};

AlertMessageView.prototype.show = function (message, messageType, undo) {
  this.alertMessageElement.removeClass('-success -fail -default');
  this.alertMessageElement.addClass('-' + messageType);
  this.messageElement.text(message);
  this.alertMessageElement.addClass('-show');
};
