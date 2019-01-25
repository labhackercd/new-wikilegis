/*global $ events getCookie setCookie opinionModalView */

var OpinionOnboardingView = function() {};

OpinionOnboardingView.prototype.initEvents = function(opinionModalView) {
  this.opinionOnboardingElement = $('.js-opinionOnboarding');
  this.buttonElement = $('.js-opinionOnboarding .js-button');
  this.cookieName = 'opinionOnboardingCookie';
  this.opinionModalView = opinionModalView;
  this.subscribers();
  this.publishers();
};

OpinionOnboardingView.prototype.publishers = function() {
  var cookie = getCookie(this.cookieName);
  if (!cookie) {
    events.showOpinionOnboarding.publish();
  } else {
    events.openOpinionModal.publish(null);
  }

  this.buttonElement.on('click', function() {
    events.closeOpinionOnboarding.publish();
  });
};

OpinionOnboardingView.prototype.subscribers = function() {
  var self = this;

  events.showOpinionOnboarding.subscribe(function() {
    self.showOnboarding();
  });

  events.closeOpinionOnboarding.subscribe(function() {
    self.closeOnboarding();
  });
};

OpinionOnboardingView.prototype.showOnboarding = function() {
  this.opinionOnboardingElement.addClass('-show');
};


OpinionOnboardingView.prototype.closeOnboarding = function() {
  this.opinionOnboardingElement.removeClass('-show');
  setCookie(this.cookieName, true);
  if (opinionModalView.hasActiveOpinionCards()) {
    events.openOpinionModal.publish(null);
  }
};