/*global $ events */

var TimelineSidebarView = function() {};

TimelineSidebarView.prototype.initEvents = function () {
  this.timelineSidebar = $('.js-timelineSidebar');

  this.subscribers();
  this.publishers();
};

TimelineSidebarView.prototype.subscribers = function () {
  var self = this;

  events.documentSaved.subscribe(function(data) {
    self.timelineSidebar.html(data.timelineHTML);
    self.updateURLParameters(data.version.number);
  });
};

TimelineSidebarView.prototype.publishers = function () {
  var self = this;
  self.timelineSidebar.on('click', '.js-namedVersion', function(event) {
    var target = $(event.target);
    var namedVersion = target.closest('.js-namedVersions');

    if (!self.timelineSidebar.hasClass('js-comparing')) {
      self.activateNamedVersion(namedVersion);
    } else {
      var compareCheckbox = namedVersion.find('.js-compareCheckbox .js-checkboxElement');
      if (compareCheckbox.attr('checked')) {
        compareCheckbox.removeAttr('checked');
      } else {
        if (self.timelineSidebar.find('.js-compareCheckbox .js-checkboxElement:checked').length < 2) {
          compareCheckbox.attr('checked', true);
        }
      }
      events.versionSelectedToCompare.publish();
    }
  });

  self.timelineSidebar.on('click', '.js-showAutosaves', function(event) {
    var target = $(event.target);
    var namedVersion = target.closest('.js-namedVersions');
    self.toggleAutosaves(namedVersion);
  });

  self.timelineSidebar.on('click', '.js-version', function(event) {
    event.preventDefault();
    if (!self.timelineSidebar.hasClass('js-comparing')) {
      var version = $(event.target).closest('.js-version');

      if (!version.hasClass('-selected')) {
        self.activateVersion(version);
      }
    }
  });
};

TimelineSidebarView.prototype.collapseAutosaves = function() {
  this.timelineSidebar.find('.js-autosaves').removeClass('-show');
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

  this.updateURLParameters(version.data('versionNumber'));
  events.loadDocumentText.publish();
};

TimelineSidebarView.prototype.updateURLParameters = function(versionNumber) {
  var newURL = window.location.protocol + '//' + window.location.host + window.location.pathname;
  var searchParams = new URLSearchParams(window.location.search);
  searchParams.set('version', versionNumber);
  newURL = newURL + '?' + searchParams.toString();
  window.history.replaceState(null, null, newURL);
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
    namedVersion.find('.js-showAutosaves').removeClass('-active');
    namedVersion.removeClass('-expanded');
  } else {
    autosaves.addClass('-show');
    namedVersion.find('.js-showAutosaves').addClass('-active');
    namedVersion.addClass('-expanded')
  }

};
