/*global $ events */

var DocumentExcerptView = function() {};

DocumentExcerptView.prototype.initEvents = function() {
  this.documentBodyElement = $('.js-documentBody');
  this.selectedHTML = undefined;
  this.lastExcerpt = undefined;
  this.publishers();
  this.subscribers();
};

DocumentExcerptView.prototype.publishers = function() {
  var self = this;

  self.documentBodyElement.on('selectstart', '.js-documentExcerpt', {}, function(e) {
    var target = $(e.target);

    if (self.documentBodyElement.data('selectionEnabled')) {
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
    }
  });

};

DocumentExcerptView.prototype.subscribers = function() {
  var self = this;

  $.Topic(events.startTextSelection).subscribe(function(excerptId) {
    self.enableSelectedExcerpt(excerptId);
  });

  $.Topic(events.cancelTextSelection).subscribe(function() {
    self.removeEnabledClass();
    self.cancelTextSelection();
  });

  $.Topic(events.suggestionCreated).subscribe(function(excerptId, html) {
    self.updateHTML(excerptId, html);
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

DocumentExcerptView.prototype.cancelTextSelection = function() {
  var selection = document.getSelection();
  selection.removeAllRanges();
};

DocumentExcerptView.prototype.updateHTML = function(excerptId, html) {
  var excerpt = $('.js-documentExcerpt[data-id="' + excerptId + '"]');
  excerpt.replaceWith(html);
  $.Topic(events.cancelTextSelection).publish();
};