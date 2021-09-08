/*global $ events */

var NavBurgerView = function() {};

NavBurgerView.prototype.initEvents = function() {
  this.publishers();
};

NavBurgerView.prototype.publishers = function() {
  $('.nav-burger').click(function() {
    if ($('body').hasClass('-open-menu')) {
      events.closeMenu.publish();
    } else {
      events.openMenu.publish();
    }
  });
};
