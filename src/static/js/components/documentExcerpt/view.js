/*global $ events */

var DocumentExcerptView = function() {};

DocumentExcerptView.prototype.initEvents = function() {
  this.publishers();
  this.subscribers();
};

DocumentExcerptView.prototype.publishers = function() {
  $('.js-document-excerpt').on('selectstart', function(e) {
    var target = $(e.target);

    if (!$('body').hasClass('-voidselect')) {
      $.Topic(events.startTextSelection).publish(target.data('id'));
    }

    if (target.closest('.js-document').hasClass('-suppress')) {
      $.Topic(events.cancelTextSelection).publish();
    }
  });

  $('.js-document-excerpt').on('mouseup', function() {
    $.Topic(events.endTextSelection).publish();
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
  var excerpts = $('.js-document-excerpt');
  excerpts.removeClass('-enabled');

  var excerpt = $('.js-document-excerpt[data-id="' + excerptId + '"]');
  excerpt.addClass('-enabled');
};

DocumentExcerptView.prototype.removeEnabledClass = function() {
  $('.js-document-excerpt').removeClass('-enabled');
};