/*global $ events */

var BodyView = function() {};

BodyView.prototype.initEvents = function() {
  this.publishers();
  this.subscribers();
  this.previousSelectedText = '';
  this.startedClick = false;
};

BodyView.prototype.publishers = function() {
  var self = this;
  $('body').on('click', function(e) {
    var target = $(e.target);
    var suggestionInput = target.closest('.js-suggestionInput');
    var opinionModal = target.closest('.js-opinionModal');

    if (!target.hasClass('js-overlay')) {
      if (suggestionInput.length === 0 && opinionModal.length === 0) {
        var selectedText = window.getSelection().toString();
        if (selectedText === '' || selectedText === self.previousSelectedText) {
          events.cancelTextSelection.publish();
        }
        self.previousSelectedText = selectedText;
      }
    }

    if (target.hasClass('js-body') && target.hasClass('js-overlay')) {
      events.closeModal.publish();
    }
  });

  $('body').on('mousedown', function(e) {
    if (!$(e.target).hasClass('js-documentExcerpt')) {
      self.startedClick = true;
      events.outsideDocumentMouseDown.publish();
    }
  });

  $('body').on('mouseup', function() {
    if (self.startedClick) {
      self.startedClick = false;
      events.outsideDocumentMouseUp.publish();
    }
  });
};

BodyView.prototype.subscribers = function() {
  var self = this;

  events.cancelTextSelection.subscribe(function() {
    self.enableUserSelection();
  });

  events.startTextSelection.subscribe(function() {
    self.disableUserSelection();
  });

  events.endTextSelection.subscribe(function() {
    self.enableUserSelection();
  });

  events.openMenu.subscribe(function() {
    self.openMenu();
  });

  events.closeMenu.subscribe(function() {
    self.closeMenu();
  });

  events.openOpinionModal.subscribe(function() {
    self.disableScroll();
  });

  events.closeModal.subscribe(function() {
    self.enableScroll();
  });

  events.openFilterModal.subscribe(function() {
    self.disableScroll();
  });
};


BodyView.prototype.disableUserSelection = function() {
  $('body').addClass('-voidselect');
};

BodyView.prototype.enableUserSelection = function() {
  $('body').removeClass('-voidselect');
};

BodyView.prototype.openMenu = function() {
  $('body').addClass('-open-menu');
};

BodyView.prototype.closeMenu = function() {
  $('body').removeClass('-open-menu');
};

BodyView.prototype.disableScroll = function() {
  $('body').addClass('-no-scroll');
  $('body').addClass('js-overlay');
};

BodyView.prototype.enableScroll = function() {
  $('body').removeClass('-no-scroll');
  $('body').removeClass('js-overlay');
};
