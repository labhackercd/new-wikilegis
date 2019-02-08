/*global $ events */

var DocumentExcerptView = function() {};

DocumentExcerptView.prototype.initEvents = function() {
  this.documentBodyElement = $('.js-documentBody');
  this.selectedHTML = undefined;
  this.lastExcerpt = undefined;
  this.selectedText = '';
  this.selectionEndTimeout = null;
  this.publishers();
  this.subscribers();
};

DocumentExcerptView.prototype.publishers = function() {
  var self = this;
  var selectionEnabled = self.documentBodyElement.data('selectionEnabled');

  self.documentBodyElement.on('mousedown touchstart', '.js-documentExcerpt', {}, function(e) {
    var target = $(e.target);

    if (selectionEnabled) {
      events.cancelTextSelection.publish();

      if (!$('body').hasClass('-voidselect')) {
        events.startTextSelection.publish(target.data('id'));
      }
    }

    if (target.closest('.js-document').hasClass('-suppress')) {
      events.cancelTextSelection.publish();
    }

    $(document).on('selectionchange', function() {
      if (this.selectionEndTimeout) {
        clearTimeout(this.selectionEndTimeout);
      }

      this.selectionEndTimeout = setTimeout(function () {
        if (document.getSelection().toString() != '') {
          $(document).unbind('selectionchange');
          events.endTextSelection.publish();
          $(document).unbind('selectionchange');
        }
      }, 500);
    });
  });

  $('.js-opinionButton').on('click', function(e) {
    events.openOpinionModal.publish($(e.target).closest('.js-opinionButton').data('excerptId'));
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
