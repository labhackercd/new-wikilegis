/*global $ events */

var CompareVersionsView = function() {};

CompareVersionsView.prototype.initEvents = function(timelineSidebar) {
  this.timelineSidebar = timelineSidebar;
  this.compareVersionAction = $('.js-compareVersionAction');
  this.showDiffButton = $('.js-showDiff');

  this.subscribers();
  this.publishers();
};

CompareVersionsView.prototype.subscribers = function() {
  var self = this;
  events.versionSelectedToCompare.subscribe(function() {
    self.toggleShowDiffButton();
  });
};

CompareVersionsView.prototype.publishers = function() {
  var self = this;
  self.compareVersionAction.on('click', function() {
    self.toggleAction();
  });
};

CompareVersionsView.prototype.toggleShowDiffButton = function() {
  if (this.timelineSidebar.timelineSidebar.find('.js-compareCheckbox .js-checkboxElement:checked').length < 2) {
    this.showDiffButton.addClass('-red');
    this.showDiffButton.removeClass('-green');
    this.showDiffButton.removeClass('js-disabled');
  } else {
    this.showDiffButton.removeClass('-red');
    this.showDiffButton.addClass('-green');
    this.showDiffButton.addClass('js-disabled');
  }
};

CompareVersionsView.prototype.toggleAction = function() {
  if (this.compareVersionAction.hasClass('js-compare')) {
    this.compareVersionAction.removeClass('js-compare');
    this.compareVersionAction.text('CANCELAR');
    this.timelineSidebar.timelineSidebar.find('.js-compareCheckbox').removeClass('_hidden');
    this.timelineSidebar.collapseAutosaves();
    this.timelineSidebar.timelineSidebar.addClass('js-comparing');
    this.showDiffButton.removeClass('_hidden');

    this.timelineSidebar.timelineSidebar.find('.js-compareCheckbox .js-checkboxElement').removeAttr('checked');
    var selectedVersion = $('.js-timelineSidebar .js-version.-selected');
    var namedParent = selectedVersion.closest('.js-namedVersions');
    namedParent.find('.js-namedVersion').addClass('-selected');
    namedParent.find('.js-compareCheckbox .js-checkboxElement').attr('checked', true);
    events.versionSelectedToCompare.publish();
  } else {
    this.compareVersionAction.addClass('js-compare');
    this.compareVersionAction.text('COMPARAR');
    $('.js-timelineSidebar .js-compareCheckbox').addClass('_hidden');
    this.timelineSidebar.timelineSidebar.removeClass('js-comparing');
    this.showDiffButton.addClass('_hidden');
  }
};