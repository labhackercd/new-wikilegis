/*global $ events */

var SearchInputView = function() {};

SearchInputView.prototype.initEvents = function() {
  this.searchInputScrollOnClick();
};

SearchInputView.prototype.searchInputScrollOnClick = function () {
  $('.js-search').on('click', function(event) {
    $([document.documentElement, document.body]).animate({scrollTop: $('.js-search').offset().top - 60}, 200);
  });
};
