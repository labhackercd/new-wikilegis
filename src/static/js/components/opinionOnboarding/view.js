/*global $ events getCookie */

var OpinionOnboardingView = function() {};

OpinionOnboardingView.prototype.initEvents = function() {
  this.opinionOnboardingElement = $('.js-opinionOnboarding');
  this.buttonElement = $('.js-opinionOnboarding .js-button');
  this.cookieName = 'opinionOnboardingCookie';
  this.subscribers();
  this.publishers();
};

OpinionOnboardingView.prototype.publishers = function() {
  var cookie = getCookie(this.cookieName);
  if (!cookie) {
    events.showOpinionOnboarding.publish();
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
  events.openOpinionModal.publish(null);
};