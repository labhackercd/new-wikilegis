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
  events.closeModal.subscribe(function() {
    self.hide();
  });
};

AppModalView.prototype.publishers = function() {
  $('.app-modal .js-closeModal').on('click', function() {
    events.closeModal.publish();
  });

  $(document).on('keydown', function(e) {
    if (e.keyCode == 27) {
      events.closeModal.publish();
    };
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
};

AppModalView.prototype.hide = function() {
  $('.app-modal').removeClass('-show');
};
