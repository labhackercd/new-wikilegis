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

    if (!target.hasClass('js-overlay') && target.closest('.js-opinionButton, .js-allOpinionsButton').length === 0) {
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

    if (target.closest('.js-notificationDropdown').length == 0) {
      events.closeNotificationList.publish();
    }

    if (target.closest('.js-textEditorWrapper').length == 0) {
      events.blurEditor.publish();
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

  events.openMenu.subscribe(function() {
    self.openMenu();
  });

  events.closeMenu.subscribe(function() {
    self.closeMenu();
  });

  events.openOpinionModal.subscribe(function() {
    if ($('.js-opinionModal .js-opinionCard').length > 0) {
      self.disableScroll();
    }
  });

  events.closeModal.subscribe(function() {
    self.enableScroll();
  });

  events.openModal.subscribe(function() {
    self.disableScroll();
  });

  events.openFilterModal.subscribe(function() {
    self.disableScroll();
  });

  events.openInfoModal.subscribe(function() {
    self.disableScroll();
  });

  events.closeFilterModal.subscribe(function() {
    self.enableScroll();
  });

  events.closeOpinionModal.subscribe(function() {
    self.enableScroll();
  });

  events.openAppOnboarding.subscribe(function() {
    self.disableScroll();
  });

  events.closeAppOnboarding.subscribe(function() {
    self.enableScroll();
  });

  events.openValidationModal.subscribe(function() {
    self.disableScroll();
  });

  events.closeValidationModal.subscribe(function() {
    self.enableScroll();
  });

  events.openConfirmFormModal.subscribe(function() {
    self.disableScroll();
  });

  events.closeConfirmFormModal.subscribe(function() {
    self.enableScroll();
  });

  events.openPublicFormModal.subscribe(function() {
    self.disableScroll();
  });

  events.closePublicFormModal.subscribe(function() {
    self.enableScroll();
  });

  events.openPublicInfoModal.subscribe(function() {
    self.disableScroll();
  });

  events.closePublicInfoModal.subscribe(function() {
    self.enableScroll();
  });

  events.openFeedbackFormModal.subscribe(function () {
    self.disableScroll();
  });

  events.closeFeedbackFormModal.subscribe(function () {
    self.enableScroll();
  });

  events.openFeedbackInfoModal.subscribe(function () {
    self.disableScroll();
  });

  events.closeFeedbackInfoModal.subscribe(function () {
    self.enableScroll();
  });

  events.openFeedbackWaitingModal.subscribe(function () {
    self.disableScroll();
  });

  events.closeFeedbackWaitingModal.subscribe(function () {
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
