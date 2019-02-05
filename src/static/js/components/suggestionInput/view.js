/*global $ events */

var SuggestionInputView = function() {};

SuggestionInputView.prototype.initEvents = function() {
  this.suggestionInputElement = $('.js-suggestionInput');
  this.selectedTextElement = $('.js-suggestionInput .js-selectedText');
  this.inputElement = $('.js-suggestionInput .js-input');
  this.inputErrorElement = $('.js-suggestionInput .js-inputError');
  this.selectedExcerpt = undefined;
  this.startIndex = undefined;
  this.endIndex = undefined;
  this.charMaxLimit = 400;
  this.subscribers();
  this.publishers();
};

SuggestionInputView.prototype.subscribers = function() {
  var self = this;

  events.endTextSelection.subscribe(function() {
    self.showInput();
    events.activateOpinionCards.publish(self.selectedExcerpt.data('id'));
    self.displayOpinionButton();
  });

  events.cancelTextSelection.subscribe(function() {
    self.hideInput();
  });

  events.showSuggestionInputError.subscribe(function(message) {
    self.showInputError(message);
  });
};

SuggestionInputView.prototype.publishers = function() {
  var self = this;

  $('.js-suggestionInput .js-close').on('click', function() {
    events.cancelTextSelection.publish();
  });

  $('.js-suggestionInput .js-send').on('click', function() {
    self.sendSuggestion();
  });

  $('.js-suggestionInput .js-opinionButton').on('click', function() {
    events.openOpinionModal.publish(self.selectedExcerpt.data('id'));
  });

  self.inputElement.on('keypress', function() {
    if ($(this).val().length > self.charMaxLimit - 1) {
      self.showInputError('Muito grande');
      return false;
    }
  });

  self.inputElement.on('keydown', function() {
    if ($(this).val().length <= self.charMaxLimit) {
      self.hideInputError();
    }
  });
};

SuggestionInputView.prototype.cleanSuggestionInput = function() {
  var self = this;

  self.selectedTextElement.text('');
  self.inputElement.val('');
  self.hideInputError();
  self.selectedExcerpt = undefined;
  self.startIndex = undefined;
  self.endIndex = undefined;
};

SuggestionInputView.prototype.showInput = function() {
  var self = this;

  if (self.suggestionInputElement.hasClass('-show')) {
    self.hideInput();
  }

  var selection = document.getSelection();
  var range = selection.getRangeAt(0);
  self.selectedExcerpt = $(range.startContainer.parentNode).closest('.js-documentExcerpt');

  if (self.selectedExcerpt.children().length > 0) {
    var fromIndex = self.selectedExcerpt.text().indexOf(range.startContainer.wholeText);
    self.startIndex = self.selectedExcerpt.text().indexOf(selection.toString(), fromIndex);
    self.endIndex = self.startIndex + selection.toString().length;
  } else {
    self.startIndex = range.startOffset;
    self.endIndex = range.endOffset;
  }

  self.selectedTextElement.text(selection.toString());
  self.suggestionInputElement.addClass('-show');
};

SuggestionInputView.prototype.hideInput = function() {
  var self = this;

  self.suggestionInputElement.removeClass('-show');
  self.cleanSuggestionInput();
};

SuggestionInputView.prototype.showInputError = function(errorMessage) {
  var self = this;

  self.inputErrorElement.text(errorMessage);
  self.inputErrorElement.addClass('-show');
};

SuggestionInputView.prototype.hideInputError = function() {
  var self = this;

  self.inputErrorElement.text('');
  self.inputErrorElement.removeClass('-show');
};

SuggestionInputView.prototype.sendSuggestion = function() {
  var self = this;

  var suggestion = self.inputElement.val();
  if (suggestion.length === 0) {
    self.showInputError('Em branco');
  } else if (suggestion.length > self.charMaxLimit) {
    self.showInputError('Muito grande');
  } else {
    var excerptId = self.selectedExcerpt.data('id');
    var groupId = $('.js-documentBody').data('groupId');

    events.sendSuggestion.publish(
      groupId,
      excerptId,
      self.startIndex,
      self.endIndex,
      suggestion
    );
  }
};


SuggestionInputView.prototype.displayOpinionButton = function() {
  if ($('.js-opinionModal .js-opinionCard.-active').length > 0) {
    $('.js-suggestionInput .js-opinionButton').removeClass('_hide');
  } else {
    $('.js-suggestionInput .js-opinionButton').addClass('_hide');
  }
};