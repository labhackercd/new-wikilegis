/*global $ */

var TextInputView = function() {};

TextInputView.prototype.initEvents = function() {
  this.textInputElement = $('input, textarea');
  this.publishers();
};

TextInputView.prototype.publishers = function() {
  var self = this;

  self.textInputElement.on('focus', function(e){
    self.addFill($(e.target));
  });

  self.textInputElement.on('blur', function(e){
    if($(this).val()=='') {
      self.removeFill($(e.target));
    }
  });

  $(window).on('load', function() {
    self.textInputElement.each(function() {
      if($(this).val()=='') {
        self.removeFill($(this));
      } else {
        self.addFill($(this));
      }
    });
  });
};

TextInputView.prototype.addFill = function(inputElement) {
  inputElement.parent().addClass('-filled');
};

TextInputView.prototype.removeFill = function(inputElement) {
  inputElement.parent().removeClass('-filled');
};
