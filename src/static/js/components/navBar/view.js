/*global $ events */

var NavBarView = function() {};

NavBarView.prototype.initEvents = function() {
  if (!$('.js-navbar').hasClass('js-owner')) {
    this.addShadowOnScroll();
  }
  this.subscribers();
};

NavBarView.prototype.subscribers = function() {
  var self = this;
  events.documentTitleEditionEnd.subscribe(function(newTitle) {
    if (newTitle != '') {
      self.updateTitle(newTitle);
      document.title = newTitle;
    }
  });

  events.documentSaved.subscribe(function(data) {
    self.updateCurrentVersion(data);
  });

  events.documentTextLoaded.subscribe(function(data) {
    $('.js-navbar .js-versionName').text(data.versionName);
  });
};

NavBarView.prototype.updateCurrentVersion = function(data) {
  var versionName = $('.js-navbar .js-versionName');
  if (data.version.name != null) {
    versionName.text(data.version.name);
  } else {
    versionName.text(data.version.time + ' - ' + data.version.date)
  }

  $('.js-navbar .js-versionsList').html(data.dropdownHTML);
};

NavBarView.prototype.addShadowOnScroll = function () {
  $(window).scroll(function() {
    var scroll = $(window).scrollTop();
    if (scroll >= 20) {
      $('.nav-bar').addClass('-shadow');
    } else {
      $('.nav-bar').removeClass('-shadow');
    }
  });
};

NavBarView.prototype.updateTitle = function(newTitle) {
  $('.js-navbar .js-documentTitle').text(newTitle);
};