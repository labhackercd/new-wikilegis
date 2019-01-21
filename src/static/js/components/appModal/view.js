/*global $ events */

var AppModalView = function() {};

AppModalView.prototype.initEvents = function() {
  this.addShadowOnScroll();
  this.subscribers();
  this.publishers();
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

AppModalView.prototype.subscribers = function() {
  var self = this;
  events.closeModal.subscribe(function(modal) {
    self.hide(modal);
  })
};

AppModalView.prototype.publishers = function() {
  $('.app-modal .js-closeModal').on('click', function(e) {
    events.closeModal.publish();
  })
};

AppModalView.prototype.hide = function(modal) {
  $('.app-modal').removeClass('-show');
};
