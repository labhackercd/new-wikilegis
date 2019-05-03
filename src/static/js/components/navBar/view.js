/*global $ events */

var NavBarView = function() {};

NavBarView.prototype.initEvents = function() {
  if (!$('.js-navbar').hasClass('js-owner')) {
    this.addShadowOnScroll();
  }
  this.subscribers();
};

NavBarView.prototype.subscribers = function() {
  var self = this;
  events.documentTitleEditionEnd.subscribe(function(newTitle) {
    self.updateTitle(newTitle);
  });
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

NavBarView.prototype.updateTitle = function(newTitle) {
  $('.js-navbar .js-documentTitle').text(newTitle);
};