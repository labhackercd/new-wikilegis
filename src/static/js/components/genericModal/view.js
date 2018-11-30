/*global $ */

var GenericModalView = function() {};

GenericModalView.prototype.initEvents = function() {
  this.addShadowOnScroll();
};

GenericModalView.prototype.addShadowOnScroll = function () {
  $('.generic-modal').scroll(function() {
    var scroll = $('.generic-modal').scrollTop();
    if (scroll >= 1) {
      $('.js-headerModal').addClass('-shadow');
    } else {
      $('.js-headerModal').removeClass('-shadow');
    }
  });
};
