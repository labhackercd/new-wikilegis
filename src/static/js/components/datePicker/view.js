/*global $ events */

var DatePickerView = function() {};

DatePickerView.prototype.initEvents = function() {
  this.publishers();
};

DatePickerView.prototype.publishers = function () {
  $('.js-datePicker').datepicker({
    language: 'pt-BR',
    minDate: new Date(),
    autoClose: true,
  })
};
