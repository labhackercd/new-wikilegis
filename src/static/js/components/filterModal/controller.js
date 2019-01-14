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
  localStorage.setItem('theme', themes);
  $.Topic(events.updateSearchParticipants).publish();
};