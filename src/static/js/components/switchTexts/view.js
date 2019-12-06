/* global $ events */

var SwitchTexts = function() {};

SwitchTexts.prototype.initEvents = function() {
	this.original = $('.diff .original');
	this.diferencas = $('.diff .diferencas');
	this.final = $('.diff .final');
	let obj = { "diffText": "Texto de diferencas entre as versoes",
		"originalText":  "Texto original sem diferencas",
		"finalText": "Texto final com alteracoes populares" };
	this.alternateTexts(obj);
}

SwitchTexts.prototype.alternateTexts = function(obj) {
	this.original.on("click", function(texto) {
		$('.diff .texto').text(obj.originalText);
	});
	this.diferencas.on("click", function(texto) {
		$('.diff .texto').text(obj.diffText);
	});
	this.final.on("click", function(texto) {
		$('.diff .texto').text(obj.finalText);
	});
	$(document).ready(function(texto) {
		$('.diff .texto').text(obj.diffText);
	});
}