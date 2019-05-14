/*global $ events autosize */

var SaveMessageView = function() {};

SaveMessageView.prototype.initEvents = function() {
  this.subscribers();
}

SaveMessageView.prototype.subscribers = function() {
  var self = this;

  events.updateSaveMessage.subscribe(function (dateString) {
    $('.js-saveMessage').removeClass('-saving');
    $('.js-saveMessage .js-timestamp').text(dateString);
  });

  events.documentChanged.subscribe(function() {
    $('.js-saveMessage').addClass('-saving');
  });
};