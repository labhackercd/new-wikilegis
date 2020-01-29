/*globals $:false */

var SwitchTexts = function () { };

SwitchTexts.prototype.initEvents = function () {
  this.original = $('.diff .original');
  this.diferencas = $('.diff .diferencas');
  this.final = $('.diff .final');
  let obj = {
    'diffText': 'Texto <span class="deleted">de diferencas </span><span class="added">entre as</span> versoes',
    'originalText': 'Texto original sem diferencas',
    'finalText': 'Texto final com alteracoes populares'
  };
  this.alternateTexts(obj);
};

SwitchTexts.prototype.alternateTexts = function (obj) { // eslint-disable-line no-unused-vars
  this.original.on('click', function (obj) {
    $('.diff .texto').html(obj.originalText);
    $('#diff').css('display', 'none');
    $('#final').css('display', 'none');
    $('#original').css('display', 'block');
    document.getElementById('diffItem').classList.remove('initialStyle');
  });
  this.diferencas.on('click', function (obj) {
    $('.diff .texto').html(obj.diffText);
    $('#original').css('display', 'none');
    $('#final').css('display', 'none');
    $('#diff').css('display', 'block');
    document.getElementById('diffItem').classList.remove('initialStyle');
  });
  this.final.on('click', function (obj) {
    $('.diff .texto').text(obj.finalText);
    $('#diff').css('display', 'none');
    $('#original').css('display', 'none');
    $('#final').css('display', 'block');
    document.getElementById('diffItem').classList.remove('initialStyle');
  });
  $(document).ready(function (obj) {
    $('.diff .texto').html(obj.diffText);
    $('#diff').css('display', 'block');
    document.getElementById('diffItem').classList.add('initialStyle');

  });
};