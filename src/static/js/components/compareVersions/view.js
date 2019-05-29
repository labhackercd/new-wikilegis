/*global $ events */

var CompareVersionsView = function() {};

CompareVersionsView.prototype.initEvents = function(timelineSidebar, controller) {
  this.timelineSidebar = timelineSidebar;
  this.controller = controller;
  this.compareVersionAction = $('.js-compareVersionAction');
  this.showDiffButton = $('.js-showDiff');
  this.versionsData = [];

  this.subscribers();
  this.publishers();
};

CompareVersionsView.prototype.subscribers = function() {
  var self = this;
  events.versionSelectedToCompare.subscribe(function() {
    self.toggleShowDiffButton();
  });

  events.textVersionLoaded.subscribe(function(data) {
    self.updateVersionDataList(data);
  });

  events.closeDiff.subscribe(function() {
    self.versionsData = [];
  });
};

CompareVersionsView.prototype.publishers = function() {
  var self = this;
  self.compareVersionAction.on('click', function() {
    self.toggleAction();
  });

  self.showDiffButton.on('click', function() {
    if (!self.showDiffButton.hasClass('js-disabled')) {
      self.fetchVersionsData();
    }
  });
};

CompareVersionsView.prototype.fetchVersionsData = function() {
  var self = this;
  var checked = self.timelineSidebar.timelineSidebar.find('.js-compareCheckbox .js-checkboxElement:checked');
  var documentId = $('.js-documentEditor').data('documentId');
  var textsData = [];

  checked.sort(function(a, b) {
    var versionA = parseInt($(a).closest('.js-namedVersion').data('versionNumber'));
    var versionB = parseInt($(b).closest('.js-namedVersion').data('versionNumber'));
    if (versionA > versionB) {
      return 1;
    } else {
      return -1;
    }

    return 0;
  });

  checked.each(function(idx, element) {
    var namedVersion = $(element).closest('.js-namedVersion');
    self.controller.loadDiffText(documentId, namedVersion.data('versionNumber'));
  });
};

CompareVersionsView.prototype.updateVersionDataList = function(data) {
  this.versionsData.push(data);
  if (this.versionsData.length === 2) {
    events.showDiff.publish(this.versionsData[0], this.versionsData[1]);
  }
};

CompareVersionsView.prototype.toggleShowDiffButton = function() {
  if (this.timelineSidebar.timelineSidebar.find('.js-compareCheckbox .js-checkboxElement:checked').length < 2) {
    this.showDiffButton.addClass('-gray');
    this.showDiffButton.removeClass('-green');
    this.showDiffButton.addClass('js-disabled');
  } else {
    this.showDiffButton.removeClass('-gray');
    this.showDiffButton.addClass('-green');
    this.showDiffButton.removeClass('js-disabled');
  }
};

CompareVersionsView.prototype.toggleAction = function() {
  if (this.compareVersionAction.hasClass('js-compare')) {
    this.compareVersionAction.removeClass('js-compare');
    this.compareVersionAction.text('CANCELAR');
    this.timelineSidebar.timelineSidebar.find('.js-compareCheckbox').removeClass('_hidden');
    this.timelineSidebar.collapseAutosaves();
    this.timelineSidebar.timelineSidebar.addClass('js-comparing');
    this.showDiffButton.addClass('-show');

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
    this.showDiffButton.removeClass('-show');
  }
};