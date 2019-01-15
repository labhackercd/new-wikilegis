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
          $.Topic(events.cancelTextSelection).publish();
        }
        self.previousSelectedText = selectedText;
      }
    }

    if (target.hasClass('js-body') && target.hasClass('js-overlay')) {
      $.Topic(events.closeOpinionModal).publish(false);
      $.Topic(events.closeFilterModal).publish(false);
    }
  });

  $('body').on('mousedown', function(e) {
    if (!$(e.target).hasClass('js-documentExcerpt')) {
      self.startedClick = true;
      $.Topic(events.outsideDocumentMouseDown).publish();
    }
  });

  $('body').on('mouseup', function() {
    if (self.startedClick) {
      self.startedClick = false;
      $.Topic(events.outsideDocumentMouseUp).publish();
    }
  });
};

BodyView.prototype.subscribers = function() {
  var self = this;

  $.Topic(events.cancelTextSelection).subscribe(function() {
    self.enableUserSelection();
  });

  $.Topic(events.startTextSelection).subscribe(function() {
    self.disableUserSelection();
  });

  $.Topic(events.endTextSelection).subscribe(function() {
    self.enableUserSelection();
  });

  $.Topic(events.openMenu).subscribe(function() {
    self.openMenu();
  });

  $.Topic(events.closeMenu).subscribe(function() {
    self.closeMenu();
  });

  $.Topic(events.openOpinionModal).subscribe(function() {
    self.disableScroll();
  });

  $.Topic(events.closeOpinionModal).subscribe(function() {
    self.enableScroll();
  });

  $.Topic(events.openFilterModal).subscribe(function() {
    self.disableScroll();
  });

  $.Topic(events.closeFilterModal).subscribe(function() {
    self.enableScroll();
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
