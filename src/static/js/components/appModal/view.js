/*global $ */

var AppModalView = function() {};

AppModalView.prototype.initEvents = function() {
  this.addShadowOnScroll();
};

AppModalView.prototype.addShadowOnScroll = function () {
  $('.js-appModalContent').scroll(function() {
    var scroll = $('.js-appModalContent').scrollTop();
    if (scroll >= 1) {
      $('.js-headerModal').addClass('-shadow');
    } else {
      $('.js-headerModal').removeClass('-shadow');
    }
  });
};
