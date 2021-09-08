/*global $ events */

var HowtoButtonView = function() {};

HowtoButtonView.prototype.initEvents = function() {
  this.buttonElement = $('.js-howtoButton');

  this.publishers();
};

HowtoButtonView.prototype.publishers = function () {
  this.buttonElement.on('click', function() {
    events.openAppOnboarding.publish();
  });
};
