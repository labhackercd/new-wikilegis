/*global $ events */

var TextInputView = function() {};

TextInputView.prototype.initEvents = function() {
  this.textInputElement = $('input, textarea');
  this.subscribers();
  this.publishers();
};

TextInputView.prototype.subscribers = function() {
  var self = this;
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
