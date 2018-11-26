/*global $ events */

var DocumentExcerptView = function() {};

DocumentExcerptView.prototype.initEvents = function() {
  this.publishers();
  this.subscribers();
};

DocumentExcerptView.prototype.publishers = function() {
  $('.js-documentExcerpt').on('selectstart', function(e) {
    var target = $(e.target);

    $.Topic(events.cancelTextSelection).publish();
    if (!$('body').hasClass('-voidselect')) {
      $.Topic(events.startTextSelection).publish(target.data('id'));
    }

    if (target.closest('.js-document').hasClass('-suppress')) {
      $.Topic(events.cancelTextSelection).publish();
    }

    $('body').one('mouseup', function() {
      $.Topic(events.endTextSelection).publish();
    });
  });

};

DocumentExcerptView.prototype.subscribers = function() {
  var self = this;

  $.Topic(events.startTextSelection).subscribe(function(excerptId) {
    self.enableSelectedExcerpt(excerptId);
  });

  $.Topic(events.cancelTextSelection).subscribe(function() {
    self.removeEnabledClass();
  });
};

DocumentExcerptView.prototype.enableSelectedExcerpt = function(excerptId) {
  var excerpts = $('.js-documentExcerpt');
  excerpts.removeClass('-enabled');

  var excerpt = $('.js-documentExcerpt[data-id="' + excerptId + '"]');
  excerpt.addClass('-enabled');
};

DocumentExcerptView.prototype.removeEnabledClass = function() {
  $('.js-documentExcerpt').removeClass('-enabled');
};