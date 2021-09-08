/*global $ events */

var SaveMessageView = function() {};

SaveMessageView.prototype.initEvents = function() {
  this.subscribers();
};

SaveMessageView.prototype.subscribers = function() {
  events.documentSaved.subscribe(function (data) {
    $('.js-saveMessage').removeClass('-saving');
    $('.js-saveMessage .js-timestamp').text(data.updated);
  });

  events.documentChanged.subscribe(function() {
    $('.js-saveMessage').addClass('-saving');
  });
};