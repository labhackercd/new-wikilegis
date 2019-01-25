/*global $ events Tooltip Urls */

var HighlightTooltipView = function() {};

HighlightTooltipView.prototype.initEvents = function () {
  this.tooltips = [];
  this.subscribers();
};

HighlightTooltipView.prototype.subscribers = function () {
  var self = this;
  events.openHighlightTooltip.subscribe( function(excerpt, currentId){
    self.showTooltip(excerpt, currentId);
  });

  events.closeHighlightTooltip.subscribe(function() {
    self.destroyTooltips();
  });
};

HighlightTooltipView.prototype.showTooltip = function (excerpt, currentId) {
  var self = this;
  var highlights = excerpt.find('.js-highlight').filter(function() {
    var ids = $(this).data('suggestionIds').toString().split(',');
    return ids.includes(currentId);
  });
  var highlight = highlights.first();

  $.get(Urls.suggestion_detail(currentId), function(data) {
    var tooltip = new Tooltip(
      highlight, {
        title: data.content,
        placement: 'top-end',

      }
    );
    self.tooltips.push(tooltip);
    tooltip.show();
  });
};

HighlightTooltipView.prototype.destroyTooltips = function () {
  var self = this;
  $.each(self.tooltips, function(index, tooltip) {
    tooltip.dispose();
  });
};
