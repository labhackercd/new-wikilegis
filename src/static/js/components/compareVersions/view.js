/*global $ events */

var CompareVersionsView = function() {};

CompareVersionsView.prototype.initEvents = function(timelineSidebar) {
  this.timelineSidebar = timelineSidebar;
  this.compareVersionAction = $('.js-compareVersionAction');

  this.subscribers();
  this.publishers();
};

CompareVersionsView.prototype.subscribers = function() {
};

CompareVersionsView.prototype.publishers = function() {
  var self = this;
  self.compareVersionAction.on('click', function() {
    self.toggleAction();
  });
};

CompareVersionsView.prototype.toggleAction = function() {
  if (this.compareVersionAction.hasClass('js-compare')) {
    this.compareVersionAction.removeClass('js-compare');
    this.compareVersionAction.text('CANCELAR');
    $('.js-timelineSidebar .js-compareCheckbox').removeClass('_hidden');
    this.timelineSidebar.collapseAutosaves();
    this.timelineSidebar.timelineSidebar.addClass('js-comparing');

    var selectedVersion = $('.js-timelineSidebar .js-version.-selected');
    var namedParent = selectedVersion.closest('.js-namedVersions');
    namedParent.find('.js-namedVersion').addClass('-selected');
    namedParent.find('.js-compareCheckbox .js-checkboxElement').attr('checked', true);
  } else {
    this.compareVersionAction.addClass('js-compare');
    this.compareVersionAction.text('COMPARAR');
    $('.js-timelineSidebar .js-compareCheckbox').addClass('_hidden');
  }
};