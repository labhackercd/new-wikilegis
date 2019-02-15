/*global $ events */

var AnimateScrollView = function() {};

AnimateScrollView.prototype.initEvents = function () {
  this.projectsButton = $('.js-projectsButton');

  this.subscribers();
  this.publishers();
};

AnimateScrollView.prototype.subscribers = function () {
  var self = this;

  events.scrollToPosition.subscribe(function (position, element) {
    self.scroll(position, element);
  });
};

AnimateScrollView.prototype.publishers = function () {
  var self = this;

  self.projectsButton.on('click', function() {
    var position = $('#js-projects-list').offset().top - 40;
    var element = $('HTML, BODY');

    events.scrollToPosition.publish(position, element);
  });
};

AnimateScrollView.prototype.scroll = function (position, element) {
  element.animate({ scrollTop: position }, 500);
};
