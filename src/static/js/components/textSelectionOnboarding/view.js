/*global $ events getCookie */

var TextSelectionOnboardingView = function() {};

TextSelectionOnboardingView.prototype.initEvents = function() {
  this.textSelectionOnboardingElement = $('.js-textSelectionOnboarding');
  this.buttonElement = $('.js-textSelectionOnboarding .js-button');
  this.cookieName = 'textSelectionOnboardingCookie';
  this.subscribers();
  this.publishers();
};

TextSelectionOnboardingView.prototype.publishers = function() {
  this.buttonElement.on('click', function() {
    events.closeTextSelectionOnboarding.publish();
  });
};

TextSelectionOnboardingView.prototype.subscribers = function() {
  var self = this;

  events.closeTextSelectionOnboarding.subscribe(function() {
    self.closeOnboarding();
  });

  events.closeOpinionModal.subscribe(function() {
    self.showOnboarding();
  })
};

TextSelectionOnboardingView.prototype.showOnboarding = function() {
  var cookie = getCookie(this.cookieName);
  if (!cookie) {
    this.textSelectionOnboardingElement.addClass('-show');
  }
};

TextSelectionOnboardingView.prototype.closeOnboarding = function() {
  this.textSelectionOnboardingElement.removeClass('-show');
  setCookie(this.cookieName, true);
};
