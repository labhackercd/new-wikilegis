/*globals $:false */

var SwitchTexts = function() {};

SwitchTexts.prototype.initEvents = function() {
  this.original = $('.diff .original');
  this.diferencas = $('.diff .diferencas');
  this.final = $('.diff .final');
  let obj = { 'diffText': 'Texto <span class="deleted">de diferencas </span><span class="added">entre as</span> versoes',
    'originalText':   'Texto original sem diferencas',
    'finalText': 'Texto final com alteracoes populares' };
  this.alternateTexts(obj);
};

SwitchTexts.prototype.alternateTexts = function(obj) { // eslint-disable-line no-unused-vars
  this.original.on('click', function(obj) {
    $('.diff .texto').html(obj.originalText);
  });
  this.diferencas.on('click', function(obj) {
    $('.diff .texto').html(obj.diffText);
  });
  this.final.on('click', function(obj) {
    $('.diff .texto').text(obj.finalText);
  });
  $(document).ready(function(obj) {
    $('.diff .texto').html(obj.diffText);
  });
};