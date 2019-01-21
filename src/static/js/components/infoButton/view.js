/*global $ events */

var InfoButtonView = function() {};

InfoButtonView.prototype.initEvents = function() {
  this.publishers();
};

InfoButtonView.prototype.publishers = function () {
  $('.js-infoButton').on('click', function() {
    events.openInfoModal.publish();
  })
};
