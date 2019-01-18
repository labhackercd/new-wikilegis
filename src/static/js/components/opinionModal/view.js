/*global $ events */

var OpinionModalView = function() {};

OpinionModalView.prototype.initEvents = function() {
  this.opinionModalElement = $('.js-opinionModal');
  this.closeElement = $('.js-opinionModal .js-closeModal');
  this.buttonsElements = $('.js-opinionModal .js-opinionButton');
  this.nextOpinionElement = $('.js-opinionModal .js-nextOpinion');
  this.cardsElement = $('.js-opinionModal .js-appModalContent');

  this.subscribers();
  this.publishers();
};

OpinionModalView.prototype.publishers = function() {
  var self = this;
  self.closeElement.click(function() {
    events.closeOpinionModal.publish(false);
  });

  self.nextOpinionElement.click(function() {
    events.nextOpinion.publish();
  })

  events.openOpinionModal.publish();

};

OpinionModalView.prototype.subscribers = function () {
  var self = this;
  events.openOpinionModal.subscribe(function(excerptId){
    self.show();
  });

  events.nextOpinion.subscribe(function() {
    self.showNextSuggestion();
  });
};

OpinionModalView.prototype.hide = function () {
  this.opinionModalElement.removeClass('-show');
};

OpinionModalView.prototype.show = function () {
  this.opinionModalElement.addClass('-show');
};

OpinionModalView.prototype.showNextSuggestion = function() {
  var first = this.cardsElement.children().first();
  this.cardsElement.append(first);
};
