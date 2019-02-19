/*global $ events */

var AppOnboardingView = function() {};

AppOnboardingView.prototype.initEvents = function(page) {
  this.appOnboardingElement = $('.js-appOnboarding');
  this.stepsElements = $('.js-appOnboarding .js-step');
  this.nextButtonsElements = $('.js-appOnboarding .js-next');
  this.closeElements = $('.js-appOnboarding .js-close');
  this.actionButtonElement = $('.js-appOnboarding .js-action');

  this.page = page;
  this.subscribers();
  this.publishers();
};

AppOnboardingView.prototype.subscribers = function () {
  var self = this;

  events.openAppOnboarding.subscribe(function() {
    self.show();
  });

  events.closeAppOnboarding.subscribe(function() {
    self.hide();
  });
};

AppOnboardingView.prototype.publishers = function () {
  var self = this;
  self.nextButtonsElements.on('click', function(e) {
    self.nextStep($(e.target).closest('.js-step'));
  });

  self.closeElements.on('click', function() {
    events.closeAppOnboarding.publish();
  });

  self.actionButtonElement.on('click', function() {
    self.doAction();
  })
};

AppOnboardingView.prototype.show = function () {
  this.appOnboardingElement.addClass('-show');
  this.stepsElements.removeClass('-active');
  this.stepsElements.first().addClass('-active');
};

AppOnboardingView.prototype.hide = function () {
  this.appOnboardingElement.removeClass('-show');
};

AppOnboardingView.prototype.nextStep = function (activeStep) {
  activeStep.next().addClass('-active');
  activeStep.removeClass('-active');
};

AppOnboardingView.prototype.doAction = function () {
  var self = this;
  switch (self.page) {
    case 'home':
      var position = $('#js-projects-list').offset().top - 40;
      events.closeAppOnboarding.publish();
      events.scrollToPosition.publish(position);
      break;
    case 'document':
      events.closeAppOnboarding.publish();
      break;
  }
};
