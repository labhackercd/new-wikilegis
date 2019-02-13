/*global $ events */

var AlertMessageView = function() {};

AlertMessageView.prototype.initEvents = function () {
  this.alertMessageElement = $('.js-alertMessage');
  this.actionsElement = $('.js-alertMessage .js-actions');
  this.actionLinkElement = $('.js-alertMessage .js-actions .js-actionLink');
  this.messageElement = $('.js-alertMessage .js-message');
  this.progressElement = $('.js-alertMessage .js-progress');
  this.emojiElement = $('.js-alertMessage .js-emoji');
  this.progressTimeout = null;
  this.progress = 0;
  this.emojis = {
    default: ['🙂', '🤐', '👉', '😯', '😏', '😌', '🤐', '😛', '🙃', '😉', '😶', '👋'],
    success: ['😃', '🥳', '🤩', '🎉', '🤘', '😎', '🥰', '👍', '👌', '✌️', '🤙', '👏'],
    fail: ['💩', '🥺', '😢', '🤭', '😰', '🧐', '☹️', '😱', '🥵', '😳', '👎', '😭']
  };

  this.subscribers();
  this.publishers();
};

AlertMessageView.prototype.subscribers = function () {
  var self = this;
  events.showMessage.subscribe(function (message, messageType, action) {
    if (messageType != 'success' && messageType != 'fail') {
      messageType = 'default';
    }
    self.show(message, messageType, action);
    setTimeout(function() {
      self.startProgress();
    }, 50);
  });

  events.stopAlertProgress.subscribe(function() {
    self.stopProgress();
  });

  events.pauseAlertProgress.subscribe(function() {
    self.pauseProgress();
  });

  events.resumeAlertProgress.subscribe(function() {
    self.resumeProgress();
  });
};

AlertMessageView.prototype.publishers = function() {
  var self = this;
  self.alertMessageElement.on('mouseover', function() {
    events.pauseAlertProgress.publish();
  });

  self.alertMessageElement.on('mouseleave', function() {
    events.resumeAlertProgress.publish();
  });
};

AlertMessageView.prototype.show = function (message, messageType, action) {
  this.alertMessageElement.removeClass('-success -fail -default -color');
  this.alertMessageElement.addClass('-' + messageType);
  this.messageElement.html(message);

  var random = Math.floor(Math.random() * this.emojis[messageType].length);
  this.emojiElement.html(this.emojis[messageType][random]);

  if (action) {
    this.actionsElement.removeClass('_hide');
    this.actionLinkElement.addClass('-' + action.name);
    this.actionLinkElement.text(action.text);
    this.actionLinkElement.attr('href', action.link);
  }

  this.alertMessageElement.addClass('-show');
};

AlertMessageView.prototype.startProgress = function () {
  var self = this;

  self.progressTimeout = setInterval(function() {
    self.updateProgress();
  }, 10);
};

AlertMessageView.prototype.updateProgress = function() {
  var self = this;
  if (self.progress >= 500) {
    events.stopAlertProgress.publish();
  } else {
    self.progress = self.progress + 1;
    self.progressElement.css('transform', 'scaleX(' + self.progress / 500 + ')');
  }
};

AlertMessageView.prototype.stopProgress = function () {
  var self = this;
  if (self.progressTimeout) {
    window.clearTimeout(self.progressTimeout);
  }

  self.alertMessageElement.addClass('-color');
  self.alertMessageElement.one('transitionend', function() {
    self.alertMessageElement.removeClass('-show');
    self.progress = 0;
    self.progressElement.css('transform', 'scaleX(' + self.progress / 500 + ')');
  });
};

AlertMessageView.prototype.pauseProgress = function() {
  var self = this;
  if (self.progressTimeout) {
    window.clearTimeout(self.progressTimeout);
  }
};

AlertMessageView.prototype.resumeProgress = function() {
  var self = this;
  self.progressTimeout = setInterval(function() {
    self.updateProgress();
  }, 10);
};
