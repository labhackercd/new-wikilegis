/*global $ events */

var InfoMessageView = function () {};

InfoMessageView.prototype.initEvents = function () {
  this.infoMessageElement = $('.js-infoMessage');
  this.progressElement = $('.js-infoMessage .js-progress');
  this.closeMessage = $('.js-closeMessage');
  this.progressTimeout = null;
  this.progress = 0;
  this.subscribers();
  this.publishers();
};

InfoMessageView.prototype.subscribers = function () {
  var self = this;
  setTimeout(function () {
    self.startProgress();
  }, 50);
  events.closeInfoMessage.subscribe(function () {
    self.hide();
  });
  events.pauseInfoMessageProgress.subscribe(function () {
    self.pauseProgress();
  });

  events.resumeInfoMessageProgress.subscribe(function () {
    self.resumeProgress();
  });
};

InfoMessageView.prototype.publishers = function () {
  var self = this;
  $(window).on('load', function () {
    self.infoMessageElement.addClass('-show');
  });
  self.closeMessage.on('click', function () {
    events.closeInfoMessage.publish();
  });
  self.infoMessageElement.on('mouseover', function () {
    events.pauseInfoMessageProgress.publish();
  });

  self.infoMessageElement.on('mouseleave', function () {
    events.resumeInfoMessageProgress.publish();
  });
};

InfoMessageView.prototype.hide = function () {
  this.infoMessageElement.removeClass('-show');
};

InfoMessageView.prototype.startProgress = function () {
  var self = this;

  self.progressTimeout = setInterval(function () {
    self.updateProgress();
  }, 10);
};

InfoMessageView.prototype.updateProgress = function () {
  var self = this;
  if (self.progress >= 500) {
    events.closeInfoMessage.publish();
  } else {
    self.progress = self.progress + 1;
    self.progressElement.css('transform', 'scaleX(' + self.progress / 500 + ')');
  }
};

InfoMessageView.prototype.pauseProgress = function () {
  var self = this;
  if (self.progressTimeout) {
    window.clearTimeout(self.progressTimeout);
  }
};

InfoMessageView.prototype.resumeProgress = function () {
  var self = this;
  self.progressTimeout = setInterval(function () {
    self.updateProgress();
  }, 10);
};