/*global $ */

var GenericModalView = function() {};

GenericModalView.prototype.initEvents = function() {
  this.addShadowOnScroll();
};

GenericModalView.prototype.addShadowOnScroll = function () {
  $('.js-genericModalContent').scroll(function() {
    var scroll = $('.js-genericModalContent').scrollTop();
    if (scroll >= 1) {
      $('.js-headerModal').addClass('-shadow');
    } else {
      $('.js-headerModal').removeClass('-shadow');
    }
  });
};
