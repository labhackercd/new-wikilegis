/*global $ events */

var TimelineSidebarView = function() {};

TimelineSidebarView.prototype.initEvents = function () {
  this.timelineSidebar = $('.js-timelineSidebar');
  this.namedVersions = $('.js-timelineSidebar .js-namedVersions');

  this.subscribers();
  this.publishers();
};

TimelineSidebarView.prototype.subscribers = function () {
};

TimelineSidebarView.prototype.publishers = function () {
  var self = this;
  this.timelineSidebar.on('click', '.js-namedVersion', function(event) {
    var target = $(event.target);
    var namedVersion = target.closest('.js-namedVersions');
    self.activateNamedVersion(namedVersion);

    if (target.closest('.js-namedVersion')) {
      self.toggleAutosaves(namedVersion);
    }
  });

  this.timelineSidebar.on('click', '.js-version', function(event) {
    var version = $(event.target).closest('.js-version');
    self.activateVersion(version);
  });
};

TimelineSidebarView.prototype.activateVersion = function (version) {
  this.timelineSidebar.find('.js-version').removeClass('-selected');
  
  if (version.hasClass('js-namedVersion')) {
    this.timelineSidebar.find('.js-version').removeClass('-stick');
  } else {
    this.timelineSidebar.find('.js-version:not(.js-namedVersion)').removeClass('-stick');
  }
  version.addClass('-selected');
  version.addClass('-stick');
};

TimelineSidebarView.prototype.activateNamedVersion = function (namedVersion) {
  this.timelineSidebar.find('.js-namedVersions').removeClass('-active');
  namedVersion.addClass('-active');
};

TimelineSidebarView.prototype.toggleAutosaves = function (namedVersion) {
  var autosaves = namedVersion.find('.js-autosaves');
  var showing = autosaves.hasClass('-show');
  this.timelineSidebar.find('.js-autosaves').removeClass('-show');
  if (showing) {
    autosaves.removeClass('-show');
  } else {
    autosaves.addClass('-show');
  }

};
