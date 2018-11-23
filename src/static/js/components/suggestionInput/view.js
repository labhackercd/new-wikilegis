/*global $ events */

var SuggestionInputView = function() {};

SuggestionInputView.prototype.initEvents = function() {
  this.subscribers();
  this.publishers();
  this.suggestionInputElement = $('.js-suggestionInput');
  this.selectedTextElement = $('.js-suggestionInput .js-selectedText');
  this.inputElement = $('.js-suggestionInput .js-input');
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
  self.selectedTextElement.text('');
};