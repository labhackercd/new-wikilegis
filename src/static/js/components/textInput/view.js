/*global $ */

var TextInputView = function() {};

TextInputView.prototype.initEvents = function() {
  this.textInputElement = $('input, textarea');
  this.publishers();
};

TextInputView.prototype.publishers = function() {
  this.textInputElement.on('focus', function(){
    $(this).parent().addClass('-filled');
  });

  this.textInputElement.on('blur', function(){
    if($(this).val()=='') {
      $(this).parent().removeClass('-filled');
    }
  });
};
