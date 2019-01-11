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
  // TODO
  $.Topic(events.updateSearchParticipants).publish();
};