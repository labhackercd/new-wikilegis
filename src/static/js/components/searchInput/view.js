/*global $ List*/

var SearchInputView = function () { };

SearchInputView.prototype.initEvents = function () {
  this.searchInputScrollOnClick();
  this.initSearch();
};

SearchInputView.prototype.searchInputScrollOnClick = function () {
  $('.js-search').on('click', function () {
    $([document.documentElement, document.body]).animate(
      { scrollTop: $('.js-search').offset().top - 80 },
      200
    );
  });
};

SearchInputView.prototype.initSearch = function () {
  var options = {
    valueNames: ['js-title', 'js-description'],
  };

  var listObj = new List('js-projects-list', options);

  $('.js-search').on('keyup', function () {
    var searchString = $(this).val();
    listObj.search(searchString);

    if (listObj.matchingItems.length > 0) {
      $('.no-result').hide();
    } else {
      $('.no-result').show();
    }
  });
};
