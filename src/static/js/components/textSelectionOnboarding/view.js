/*global $ events getCookie setCookie */

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

  events.showTextSelectionOnboarding.subscribe(function() {
    self.showOnboarding();
  });

  events.closeTextSelectionOnboarding.subscribe(function() {
    self.closeOnboarding();
  });

  events.closeOpinionModal.subscribe(function() {
    var cookie = getCookie(self.cookieName); 
    if (!cookie && self.textSelectionOnboardingElement.data('isAuthenticated')) {
      events.showTextSelectionOnboarding.publish();
    }
  });
};

TextSelectionOnboardingView.prototype.showOnboarding = function() {
  this.textSelectionOnboardingElement.addClass('-show');
};

TextSelectionOnboardingView.prototype.closeOnboarding = function() {
  this.textSelectionOnboardingElement.removeClass('-show');
  setCookie(this.cookieName, true);
};
