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

  self.buttonsElements.click(function() {
    var buttonElement = $(this);
    var cardElement = buttonElement.closest('.js-opinionCard');
    events.sendOpinion.publish(
      cardElement.data('suggestionId'),
      buttonElement.data('opinion')
    );
  })

};

OpinionModalView.prototype.subscribers = function () {
  var self = this;
  events.openOpinionModal.subscribe(function(excerptId){
    if (self.cardsElement.children().length > 0) {
      self.show();
    }
  });

  events.closeOpinionModal.subscribe(function() {
    self.hide();
  });

  events.nextOpinion.subscribe(function() {
    self.showNextSuggestion();
  });

  events.opinionSent.subscribe(function(opinion) {
    self.opinionSent(opinion);
  })
};

OpinionModalView.prototype.hide = function () {
  this.opinionModalElement.removeClass('-show');
};

OpinionModalView.prototype.show = function () {
  this.opinionModalElement.addClass('-show');
};

OpinionModalView.prototype.showNextSuggestion = function() {
  var self = this;
  var first = self.cardsElement.children().first();
  first.addClass('-next');
  first.one('transitionend', function() {
    first.removeClass('-next');
    self.cardsElement.append(first);
  })
};

OpinionModalView.prototype.opinionSent = function(opinion) {
  var self = this;
  var card = self.cardsElement.children().first();
  card.addClass('-' + opinion);
  card.one('transitionend', function() {
    card.remove();
    if (self.cardsElement.children().length === 0) {
      events.closeOpinionModal.publish();
    }
  })
};
