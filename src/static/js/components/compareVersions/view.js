/*global $ events */

var CompareVersionsView = function() {};

CompareVersionsView.prototype.initEvents = function(timelineSidebar, controller) {
  this.timelineSidebar = timelineSidebar;
  this.controller = controller;
  this.compareActions = $('.js-compareActions');
  this.startComparisonElement = $('.js-compareActions .js-startComparison');
  this.cancelComparisonElement = $('.js-compareActions .js-cancelComparison');
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

  events.documentChanged.subscribe(function() {
    self.cancelComparison();
  });
};

CompareVersionsView.prototype.publishers = function() {
  var self = this;
  self.startComparisonElement.on('click', function() {
    if (self.startComparisonElement.hasClass('js-comparing')) {
      if (!self.startComparisonElement.hasClass('js-disabled')) {
        self.fetchVersionsData();
      }
    } else {
      self.startComparison();
    }
  });

  self.cancelComparisonElement.on('click', function() {
    self.cancelComparison();
  });
};

CompareVersionsView.prototype.fetchVersionsData = function() {
  var self = this;
  var checked = self.timelineSidebar.timelineSidebar.find('.js-compareCheckbox .js-checkboxElement:checked');
  var documentId = $('.js-documentEditor').data('documentId');

  checked.sort(function(a, b) {
    var versionA = parseInt($(a).closest('.js-namedVersion').data('versionNumber'));
    var versionB = parseInt($(b).closest('.js-namedVersion').data('versionNumber'));
    if (versionA > versionB) {
      return 1;
    } else {
      return -1;
    }
  });

  checked.each(function(idx, element) {
    var namedVersion = $(element).closest('.js-namedVersion');
    self.controller.loadDiffText(documentId, namedVersion.data('versionNumber'));
  });
};

CompareVersionsView.prototype.updateVersionDataList = function(data) {
  this.versionsData.push(data);
  if (this.versionsData.length === 2) {
    var data1 = this.versionsData[0];
    var data2 = this.versionsData[1];

    if (data1.versionNumber > data2.versionNumber) {
      events.showDiff.publish(data2, data1);
    } else {
      events.showDiff.publish(data1, data2);
    }

  }
};

CompareVersionsView.prototype.toggleShowDiffButton = function() {
  if (this.timelineSidebar.timelineSidebar.find('.js-compareCheckbox .js-checkboxElement:checked').length < 2) {
    this.startComparisonElement.addClass('-gray');
    this.startComparisonElement.removeClass('-green');
    this.startComparisonElement.addClass('js-disabled');
  } else {
    this.startComparisonElement.removeClass('-gray');
    this.startComparisonElement.addClass('-green');
    this.startComparisonElement.removeClass('js-disabled');
  }
};

CompareVersionsView.prototype.startComparison = function () {
  this.cancelComparisonElement.addClass('-show');
  this.startComparisonElement.addClass('js-comparing');

  this.timelineSidebar.timelineSidebar.find('.js-compareCheckbox').removeClass('_hidden');
  this.timelineSidebar.collapseAutosaves();
  this.timelineSidebar.timelineSidebar.addClass('js-comparing');
  this.timelineSidebar.timelineSidebar.find('.js-compareCheckbox .js-checkboxElement').removeAttr('checked');

  var selectedVersion = this.timelineSidebar.timelineSidebar.find('.js-version.-selected');
  var namedParent = selectedVersion.closest('.js-namedVersions');
  namedParent.find('.js-namedVersion').addClass('-selected');
  namedParent.find('.js-compareCheckbox .js-checkboxElement').attr('checked', true);
  events.versionSelectedToCompare.publish();
};

CompareVersionsView.prototype.cancelComparison = function () {
  this.cancelComparisonElement.removeClass('-show');
  this.startComparisonElement.removeClass('js-comparing');
  this.startComparisonElement.removeClass('-gray');
  this.startComparisonElement.addClass('-green');

  $('.js-timelineSidebar .js-compareCheckbox').addClass('_hidden');
  this.timelineSidebar.timelineSidebar.removeClass('js-comparing');
};
