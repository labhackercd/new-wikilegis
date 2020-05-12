/*global $ events */

var DocumentCardView = function() {};

DocumentCardView.prototype.initEvents = function() {
	this.documentCard();
}

DocumentCardView.prototype.subscriber = function() {
	var self = this;
	events.documentCard.subscribe(function(){
		self.documentCard();
	});
}

DocumentCardView.prototype.documentCard = function() {
	$('.js-description').each(function(x) {
    var currentText = $(this).text();
    var newText = currentText.substring(0, 300) + '...' + '<a class="pseudolink"> Veja mais! </a>';
    $(this).html(newText);
  });		
}
