/*global $ */

var appModalView = function() {};

appModalView.prototype.initEvents = function() {
  this.addShadowOnScroll();
};

appModalView.prototype.addShadowOnScroll = function () {
  $('.js-appModalContent').scroll(function() {
    var scroll = $('.js-appModalContent').scrollTop();
    if (scroll >= 1) {
      $('.js-headerModal').addClass('-shadow');
    } else {
      $('.js-headerModal').removeClass('-shadow');
    }
  });
};
