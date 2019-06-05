/*global $ pagemap */

var PageMinimap = function() {};

PageMinimap.prototype.initEvents = function() {
  this.publishers();
};

PageMinimap.prototype.publishers = function() {
  pagemap($('.js-pageMinimap')[0], {
    viewport: $('.js-documentEditor')[0],
    styles: {
      '.js-documentTitle, .js-documentDescription': 'rgba(0,0,0,0.08)',
      '.js-documentExcerpt': 'rgba(0,0,0,0.08)',
      '.js-excerptNumbering': 'rgba(0,0,0,0.03)',
      '.js-participationAmount1.js-participationActive': 'hsla(147, 58%, 90%, 1)',
      '.js-participationAmount2.js-participationActive': 'hsla(147, 58%, 80%, 1)',
      '.js-participationAmount3.js-participationActive': 'hsla(147, 58%, 70%, 1)',
      '.js-participationAmount4.js-participationActive': 'hsla(147, 58%, 60%, 1)',
      '.js-participationAmount5.js-participationActive': 'hsla(147, 58%, 50%, 1)',
      '.js-opinionsAmount1.js-opinionsActive': 'hsla(220, 60%, 90%, 1)',
      '.js-opinionsAmount2.js-opinionsActive': 'hsla(220, 60%, 80%, 1)',
      '.js-opinionsAmount3.js-opinionsActive': 'hsla(220, 60%, 70%, 1)',
      '.js-opinionsAmount4.js-opinionsActive': 'hsla(220, 60%, 60%, 1)',
      '.js-opinionsAmount5.js-opinionsActive': 'hsla(220, 60%, 50%, 1)',
      '.js-votesAmount1.js-votesActive': 'hsla(275, 100%, 90%, 1)',
      '.js-votesAmount2.js-votesActive': 'hsla(275, 100%, 80%, 1)',
      '.js-votesAmount3.js-votesActive': 'hsla(275, 100%, 70%, 1)',
      '.js-votesAmount4.js-votesActive': 'hsla(275, 100%, 60%, 1)',
      '.js-votesAmount5.js-votesActive': 'hsla(275, 100%, 50%, 1)',
    },
    back: 'rgba(0,0,0,0.03)',
    view: 'rgba(0,0,0,0.05)',
    drag: 'rgba(0,0,0,0.065)',
    interval: 50
  });
};
