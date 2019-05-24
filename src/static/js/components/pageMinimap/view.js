/*global $ pagemap */

var PageMinimap = function() {};

PageMinimap.prototype.initEvents = function() {
  this.publishers();
};

PageMinimap.prototype.publishers = function() {
  pagemap($('.js-pageMinimap')[0], {
    styles: {
      '.js-documentTitle, .js-documentDescription': 'rgba(0,0,0,0.08)',
      '.js-documentExcerpt': 'rgba(0,0,0,0.08)',
      '.js-excerptNumbering': 'rgba(0,0,0,0.03)',
      '.js-relevanceAmount1': 'hsla(275, 120%, 90%, 1)',
      '.js-relevanceAmount2': 'hsla(275, 120%, 80%, 1)',
      '.js-relevanceAmount3': 'hsla(275, 120%, 70%, 1)',
      '.js-relevanceAmount4': 'hsla(275, 120%, 60%, 1)',
      '.js-relevanceAmount5': 'hsla(275, 120%, 50%, 1)',
    },
    back: 'rgba(0,0,0,0.03)',
    view: 'rgba(0,0,0,0.05)',
    drag: 'rgba(0,0,0,0.065)',
    interval: 50
  });
};