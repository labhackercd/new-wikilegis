/*global $ events */

var DocumentExcerptView = function() {};

DocumentExcerptView.prototype.initEvents = function() {
  this.documentBodyElement = $('.js-documentBody');
  this.allOpinionsButton = $('.js-allOpinionsButton');
  this.showOpinionsButtons = $('.js-opinionButton, .js-allOpinionsButton');
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

      if (!$('body').hasClass('-voidselect') && !target.hasClass('js-highlight')) {
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

  self.showOpinionsButtons.click(function() {
    var opinionButton = $(this);
    var excerptId = null;

    if (opinionButton.is('.js-allOpinionsButton')) {
      excerptId = 'all';
    } else {
      excerptId = opinionButton.closest('.js-excerptWrapper').find('.js-documentExcerpt').data('id');
    }

    events.openOpinionModal.publish(excerptId);
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

  events.hideExcerptOpinionBalloon.subscribe(function(excerptId) {
    self.hideExcerptOpinionBalloon(excerptId);
  });

  events.hideDocumentOpinionBalloon.subscribe(function() {
    self.hideDocumentOpinionBalloon(self.allOpinionsButton);
  });

  events.suggestionUndone.subscribe(function(data) {
    self.updateHTML(data.excerptId, data.excerptHtml);
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

DocumentExcerptView.prototype.hideExcerptOpinionBalloon = function(excerptId) {
  var balloon = $('.js-documentExcerpt[data-id="' + excerptId + '"]').siblings('.js-opinionButton');
  balloon.addClass('_hide');
};

DocumentExcerptView.prototype.hideDocumentOpinionBalloon = function(allOpinionsButton) {
  allOpinionsButton.addClass('_hide');
};
