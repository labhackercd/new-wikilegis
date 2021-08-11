/*global $ events */

var AlertMessageView = function() {};

AlertMessageView.prototype.initEvents = function () {
  this.alertMessageElement = $('.js-alertMessage');
  this.actionsElement = $('.js-alertMessage .js-actions');
  this.actionLinkElement = $('.js-alertMessage .js-actions .js-actionLink');
  this.messageElement = $('.js-alertMessage .js-message');
  this.progressElement = $('.js-alertMessage .js-progress');
  this.emojiElement = $('.js-alertMessage .js-emoji');
  this.actionClasses = '-undo';
  this.progressTimeout = null;
  this.progress = 0;
  this.emojis = {
    default: ['🙂', '🤐', '👉', '😯', '😏', '😌', '🤐', '😛', '🙃', '😉', '😶', '👋'],
    success: ['😃', '🤩', '🎉', '🤘', '😎', '👍', '👌', '✌️', '🤙', '👏'],
    fail: ['😢', '🤭', '😰', '🧐', '😱', '😳', '👎', '😭', ]
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

  events.stopAlertProgress.subscribe(function(cancelAction) {
    self.stopProgress(cancelAction);
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

  self.actionLinkElement.on('click', function(e) {
    e.preventDefault();
    var target = $(e.target);
    events.activateAlertAction.publish(target.attr('href'));
  });
};

AlertMessageView.prototype.getRandomEmoji = function(messageType) {
  var random = Math.floor(Math.random() * this.emojis[messageType].length);
  return this.emojis[messageType][random];
};

AlertMessageView.prototype.show = function (message, messageType, action) {
  this.alertMessageElement.removeClass('-success -fail -default -color');
  this.alertMessageElement.addClass('-' + messageType);
  this.messageElement.html(message);

  this.emojiElement.html(this.getRandomEmoji(messageType));

  if (action) {
    this.actionsElement.removeClass('_hide');
    this.actionLinkElement.removeClass(this.actionClasses);
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

AlertMessageView.prototype.stopProgress = function (cancelAction) {
  var self = this;
  if (self.progressTimeout) {
    window.clearTimeout(self.progressTimeout);
  }

  if (cancelAction) {
    this.emojiElement.html(this.getRandomEmoji('fail'));
    self.alertMessageElement.removeClass('-success -fail');
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
