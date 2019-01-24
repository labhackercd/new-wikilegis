/*global $ events */

var HighlightTooltipView = function() {};

HighlightTooltipView.prototype.initEvents = function () {
  this.tooltips = {};
  this.subscribers();
};

HighlightTooltipView.prototype.subscribers = function () {
  var self = this;
  events.openHighlightTooltip.subscribe(function (parentNode, activeId) {
    self.showTooltip(parentNode, activeId);
  });

  events.closeHighlightTooltip.subscribe(function (parentNode) {
    self.hideTooltip(parentNode);
  });
};

HighlightTooltipView.prototype.showTooltip = function (parentNode, activeId) {
  var self = this;

  var highlight = parentNode.find('.js-highlight').filter(function() {
    var ids = $(this).data('suggestionIds').toString().split(',');
    return ids.includes(activeId);
  }).first();
  var tooltip = new Tooltip(highlight, {
    placement: 'top',
    title: highlight.data('content')
  });
  self.tooltips[highlight[0]] = tooltip;
  tooltip.show();
};


HighlightTooltipView.prototype.hideTooltip = function (parentNode) {
  var self = this;
  parentNode.find('.js-highlight').each(function(index, value) {
    self.tooltips[value].dispose();
  });
};
