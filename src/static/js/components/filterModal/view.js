/*global $ events */

var FilterModalView = function() {};

FilterModalView.prototype.initEvents = function() {
  this.filterModalElement = $('.js-filterModal');
  this.closeElement = $('.js-filterModal .js-closeModal');
  this.applyFilter = $('.js-filterModal .js-applyFilter');
  this.formElement = $('.js-filterModal .js-filterModalForm');
  this.subscribers();
  this.publishers();
};

FilterModalView.prototype.subscribers = function () {
  var self = this;
  events.openFilterModal.subscribe(function(){
    self.show();
  });

  events.closeFilterModal.subscribe(function(){
    self.hide();
  });

  events.resetFilterModalForm.subscribe(function(){
    self.resetForm();
  });
};

FilterModalView.prototype.publishers = function () {
  this.applyFilter.on('click', function() {
    events.closeFilterModal.publish(true);
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

FilterModalView.prototype.resetForm = function () {
  $('.js-filterModal .js-tags').html('');
  $('.js-filterModal .js-title').addClass('_hidden');
  $('.js-filterModal .js-inputText').removeClass('-filled');
  $('.js-filterModal input[name="themes"]').remove();
  this.formElement[0].reset();
};
