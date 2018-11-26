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
    var suggestionInput = $(e.target).closest('.js-suggestionInput');
    if (suggestionInput.length === 0) {
      var selectedText = window.getSelection().toString();
      if (selectedText === '' || selectedText === self.previousSelectedText) {
        $.Topic(events.cancelTextSelection).publish();
      }
      self.previousSelectedText = selectedText;
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
