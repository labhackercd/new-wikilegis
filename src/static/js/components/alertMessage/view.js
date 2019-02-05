/*global $ events */

var AlertMessageView = function() {};

AlertMessageView.prototype.initEvents = function () {
  this.alertMessageElement = $('.js-alertMessage');
  this.actionsElement = $('.js-alertMessage .js-actions');
  this.messageElement = $('.js-alertMessage .js-message');
  this.progressElement = $('.js-alertMessage .js-progress');
  this.progressTimeout = null;
  this.progress = 0;

  this.subscribers();
};

AlertMessageView.prototype.subscribers = function () {
  var self = this;
  events.showMessage.subscribe(function (message, messageType, undo) {
    if (messageType != 'success' && messageType != 'fail') {
      messageType = 'default';
    }
    self.show(message, messageType, undo);
    setTimeout(function() {
      self.startProgress();
    }, 1000);
  });

  events.stopAlertProgress.subscribe(function() {
    self.stopProgress();
  })
};

AlertMessageView.prototype.show = function (message, messageType, undo) {
  this.alertMessageElement.removeClass('-success -fail -default');
  this.alertMessageElement.addClass('-' + messageType);
  this.messageElement.text(message);
  this.alertMessageElement.addClass('-show');
};

AlertMessageView.prototype.startProgress = function () {
  var self = this;
  self.progress = 0;

  self.progressTimeout = setInterval(function() {
    if (self.progress >= 500) {
      events.stopAlertProgress.publish();
    } else {
      self.progress = self.progress + 1;
      self.progressElement.css('transform', 'scaleX(' + self.progress / 500 + ')');
    }
  }, 10)
};

AlertMessageView.prototype.stopProgress = function () {
  var self = this;
  if (self.progressTimeout) {
    window.clearTimeout(self.progressTimeout);
  }

  self.alertMessageElement.addClass('-hide');
  self.alertMessageElement.one('transitionend', function() {
    self.alertMessageElement.removeClass('-show -hide');
  });
};
