/*global $ events */

var filterModalController = function() {};

filterModalController.prototype.initEvents = function() {
  this.subscribers();
};

filterModalController.prototype.subscribers = function() {
  var self = this;

  $.Topic(events.closeFilterModal).subscribe(function(applyFilter) {
    if(applyFilter) {
      self.applyFilters();
    }
  });
};

filterModalController.prototype.applyFilters = function() {
  var themes = [];
  $('.js-tag').each(function(){
    themes.push($(this).data('themeId'));
  });
  var minAge = $('.js-minAge').val();
  var maxAge = $('.js-maxAge').val();
  var gender = $('.js-gender').val();
  var locale = $('.js-locale').val();
  localStorage.setItem('minAge', minAge);
  localStorage.setItem('maxAge', maxAge);
  localStorage.setItem('gender', gender);
  localStorage.setItem('locale', locale);
  $.Topic(events.updateSearchParticipants).publish();
};