/*global $ events */

var TextHighlightView = function() {};

TextHighlightView.prototype.initEvents = function () {
  this.subscribers();
  this.publishers();
};

TextHighlightView.prototype.subscribers = function () {
  var self = this;
  events.openHighlightTooltip.subscribe(function (parentNode, activeId) {
    self.activateHighlight(parentNode, activeId);
  });

  events.closeHighlightTooltip.subscribe(function (parentNode) {
    self.deactivateHighlight(parentNode);
  });
};

TextHighlightView.prototype.publishers = function () {
  var self = this;
  $('.js-documentBody').on('mouseenter', '.js-highlight', function(e) {
    var target = $(e.target);
    var currentId = target.data('suggestionIds').toString().split(',')[0];
    var excerpt = target.closest('.js-documentExcerpt');
    self.activateHighlight(excerpt, currentId);
  });

  $('.js-documentBody').on('click', '.js-highlight', function(e) {
    var target = $(e.target);
    var currentId = target.data('suggestionIds').toString().split(',')[0];
    var excerpt = target.closest('.js-documentExcerpt');
    events.openHighlightTooltip.publish(excerpt, currentId);
  });

  $('.js-documentBody').on('mouseleave', '.js-highlight', function(e) {
    events.closeHighlightTooltip.publish($(e.target).closest('.js-documentExcerpt'));
  });
};

TextHighlightView.prototype.deactivateHighlight = function (parentNode) {
  parentNode.find('.js-highlight').removeClass('-active');
};

TextHighlightView.prototype.activateHighlight = function (parent, suggestionId) {
  parent.find('.js-highlight').filter(function() {
    var ids = $(this).data('suggestionIds').toString().split(',');
    return ids.includes(suggestionId);
  }).addClass('-active');
};
