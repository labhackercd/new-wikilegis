/*global $ events */

var SuggestionInputView = function() {};

SuggestionInputView.prototype.initEvents = function() {
  this.suggestionInputElement = $('.js-suggestionInput');
  this.selectedTextElement = $('.js-suggestionInput .js-selectedText');
  this.inputElement = $('.js-suggestionInput .js-input');
  this.inputErrorElement = $('.js-suggestionInput .js-inputError');
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
  })
};

SuggestionInputView.prototype.cleanSuggestionInput = function() {
  var self = this;

  self.selectedTextElement.text('');
  self.inputElement.val('');
  self.hideInputError();
};

SuggestionInputView.prototype.showInput = function() {
  var self = this;
  var selectedText = document.getSelection().toString();

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
    $.Topic(events.sendSuggestion).publish();
  }
};