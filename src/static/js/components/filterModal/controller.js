/*global $ events */

var FilterModalController = function() {};

FilterModalController.prototype.initEvents = function() {
  this.subscribers();
};

FilterModalController.prototype.subscribers = function() {
  var self = this;

  events.closeFilterModal.subscribe(function(applyFilter) {
    if(applyFilter) {
      self.applyFilters();
    }
  });
};

FilterModalController.prototype.applyFilters = function() {
  var themes = [];
  $('.js-tag').each(function(){
    themes.push($(this).data('themeId'));
  });
  var minAge = $('.js-minAge').val();
  var maxAge = $('.js-maxAge').val();
  var gender = $('.js-gender').val();
  var locale = $('.js-locale').val();
  localStorage.setItem('theme', themes);
  localStorage.setItem('minAge', minAge);
  localStorage.setItem('maxAge', maxAge);
  localStorage.setItem('gender', gender);
  localStorage.setItem('locale', locale);
  events.updateSearchParticipants.publish();
};
