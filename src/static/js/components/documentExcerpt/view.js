/*global $ events */

var DocumentExcerptView = function() {};

DocumentExcerptView.prototype.initEvents = function() {
  this.documentBodyElement = $('.js-documentBody');
  this.selectedHTML = undefined;
  this.lastExcerpt = undefined;
  this.selectedText = '';
  this.publishers();
  this.subscribers();
};

DocumentExcerptView.prototype.publishers = function() {
  var self = this;
  var timeout = undefined;

  self.documentBodyElement.on('mousedown touchstart', '.js-documentExcerpt', {}, function(e) {
    var target = $(e.target);

    if (self.documentBodyElement.data('selectionEnabled')) {
      events.cancelTextSelection.publish();

      if (!$('body').hasClass('-voidselect')) {
        events.startTextSelection.publish(target.data('id'));
      }
    }

    if (target.closest('.js-document').hasClass('-suppress')) {
      events.cancelTextSelection.publish();
    }

    target.one('selectionend', function() {
      if (document.getSelection().toString() != '') {
        events.endTextSelection.publish();
      }
    });
  });
};

DocumentExcerptView.prototype.subscribers = function() {
  var self = this;

  events.startTextSelection.subscribe(function(excerptId) {
    self.enableSelectedExcerpt(excerptId);
  });

  events.cancelTextSelection.subscribe(function() {
    self.removeEnabledClass();
    self.cancelTextSelection();
  });

  events.suggestionCreated.subscribe(function(excerptId, html) {
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
  events.cancelTextSelection.publish();
};
