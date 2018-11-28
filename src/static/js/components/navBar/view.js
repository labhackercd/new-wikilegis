/*global $ */

var NavBarView = function() {};

NavBarView.prototype.initEvents = function() {
  this.addShadowOnScroll();
};

NavBarView.prototype.addShadowOnScroll = function () {
  $(window).scroll(function() {
    var scroll = $(window).scrollTop();
    if (scroll >= 20) {
      $('.nav-bar').addClass('-shadow');
    } else {
      $('.nav-bar').removeClass('-shadow');
    }
  });
};