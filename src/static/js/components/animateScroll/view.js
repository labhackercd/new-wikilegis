/*global $ events */

var AnimateScrollView = function() {};

AnimateScrollView.prototype.initEvents = function () {
  this.subscribers();
};

AnimateScrollView.prototype.subscribers = function () {
  var self = this;

  events.scrollToPosition.subscribe(function (position) {
    self.scroll(position);
  });
};

AnimateScrollView.prototype.scroll = function (position) {
  var element = $('HTML, BODY');
  element.animate({ scrollTop: position }, 500);
};
