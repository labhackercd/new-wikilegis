/*global $ events */

var AddExcerptView = function() {};

AddExcerptView.prototype.initEvents = function() {
  this.publishers();
};

AddExcerptView.prototype.publishers = function() {
  $('.js-documentEditor').on('click', '.js-addExcerpt .js-button', function() {
    console.log('abre opções');
    var addExcerptButton = $(this);
  });

  $('.js-documentEditor').on('click', '.js-addExcerpt .js-excerptType', function() {
    console.log('adiciona')
  });
};