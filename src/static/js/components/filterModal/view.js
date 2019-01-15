/*global $ events */

var FilterModalView = function() {};

FilterModalView.prototype.initEvents = function() {
  this.filterModalElement = $('.js-filterModal');
  this.closeElement = $('.js-filterModal .js-closeModal');
  this.applyFilter = $('.js-filterModal .js-applyFilter');
  this.subscribers();
  this.publishers();
};

FilterModalView.prototype.subscribers = function () {
  var self = this;
  $.Topic(events.openFilterModal).subscribe(function(){
    self.show();
  });

  $.Topic(events.closeFilterModal).subscribe(function(){
    self.hide();
  });
};

FilterModalView.prototype.publishers = function () {
  this.closeElement.on('click', function() {
    $.Topic(events.closeFilterModal).publish(false);
  });

  this.applyFilter.on('click', function() {
    $.Topic(events.closeFilterModal).publish(true);
  });

  $(window).on('unload', function() {
    localStorage.clear();
  });
};

FilterModalView.prototype.show = function () {
  this.filterModalElement.addClass('-show');
};

FilterModalView.prototype.hide = function () {
  this.filterModalElement.removeClass('-show');
};
