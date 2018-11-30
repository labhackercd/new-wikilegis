/*global $ events */

var OpinionModalView = function() {};

OpinionModalView.prototype.initEvents = function() {
  this.publishers();
  this.subscribers();
};

OpinionModalView.prototype.publishers = function() {
  $('.js-closeModal').click(function() {
    $.Topic(events.closeOpinionModal).publish();
  });

  $(document).ready(function(){
    $.Topic(events.openOpinionModal).publish();
  });
};

OpinionModalView.prototype.subscribers = function () {
  var self = this;

  $.Topic(events.openOpinionModal).subscribe(function(){
    self.show();
  });

  $.Topic(events.closeOpinionModal).subscribe(function(){
    self.hide();
  });
};

OpinionModalView.prototype.hide = function () {
  $('.js-opinionModal').removeClass('-show');
};

OpinionModalView.prototype.show = function () {
  $('.js-opinionModal').addClass('-show');
};
