/*global $ events */

var SuggestionInputView = function() {};

SuggestionInputView.prototype.initEvents = function() {
  this.suggestionInputElement = $('.js-suggestionInput');
  this.selectedTextElement = $('.js-suggestionInput .js-selectedText');
  this.inputElement = $('.js-suggestionInput .js-input');
  this.inputErrorElement = $('.js-suggestionInput .js-inputError');
  this.selectedExcerpt = undefined;
  this.selectionRange = undefined;
  this.charMaxLimit = 100;
  this.subscribers();
  this.publishers();
};

SuggestionInputView.prototype.subscribers = function() {
  var self = this;

  $.Topic(events.endTextSelection).subscribe(function() {
    self.showInput();
  });

  $.Topic(events.cancelTextSelection).subscribe(function() {
    self.hideInput();
  });

  $.Topic(events.showSuggestionInputError).subscribe(function(message) {
    self.showInputError(message);
  });
};

SuggestionInputView.prototype.publishers = function() {
  var self = this;

  $('.js-suggestionInput .js-close').on('click', function() {
    $.Topic(events.cancelTextSelection).publish();
  });

  $('.js-suggestionInput .js-send').on('click', function() {
    self.sendSuggestion();
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
  self.selectionRange = undefined;
};

SuggestionInputView.prototype.showInput = function() {
  var self = this;
  var selection = document.getSelection();
  var range = selection.getRangeAt(0);
  var selectedText = selection.toString();

  self.selectedExcerpt = $(range.startContainer.parentNode);
  self.selectionRange = range;

  self.selectedTextElement.text(selectedText);
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
    var startIndex = self.selectedExcerpt.text().indexOf(self.selectionRange.toString());
    var endIndex = startIndex + self.selectionRange.toString().length;

    $.Topic(events.sendSuggestion).publish(
      excerptId,
      startIndex,
      endIndex,
      suggestion
    );
  }
};