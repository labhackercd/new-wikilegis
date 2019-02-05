/*global $ events */

var OpinionModalView = function() {};

OpinionModalView.prototype.initEvents = function() {
  this.opinionModalElement = $('.js-opinionModal');
  this.buttonsElements = $('.js-opinionModal .js-opinionButton');
  this.nextOpinionElements = $('.js-opinionModal .js-nextOpinion');
  this.modalContentElement = $('.js-opinionModal .js-appModalContent');
  this.documentSuggestion = undefined;
  this.currentExcerptId = undefined;
  this.cardsElements = $('.js-opinionModal .js-opinionCard');
  this.subscribers();
  this.publishers();
};

OpinionModalView.prototype.publishers = function() {
  var self = this;

  self.nextOpinionElements.click(function() {
    self.rippleCircleButton($(this));
    events.nextOpinion.publish();
  });

  self.buttonsElements.click(function() {
    var buttonElement = $(this);
    var cardElement = buttonElement.closest('.js-opinionCard');
    self.rippleCircleButton(buttonElement);

    events.sendOpinion.publish(
      cardElement.data('suggestionId'),
      buttonElement.data('opinion'),
    );
  });

};

OpinionModalView.prototype.subscribers = function () {
  var self = this;

  events.openOpinionModal.subscribe(function(){
    if (self.modalContentElement.children('.-active').length > 0) {
      self.show();
    }
  });

  events.cancelTextSelection.subscribe(function() {
    self.hide();
  });

  events.nextOpinion.subscribe(function() {
    self.showNextSuggestion();
  });

  events.opinionSent.subscribe(function(opinion) {
    self.opinionSent(opinion);
  });

  events.activateOpinionCards.subscribe(function(excerptId) {
    self.activateOpinionCards(excerptId);
  });

  events.closeModal.subscribe(function() {
    events.closeOpinionModal.publish();
  });

  events.showNextSuggestion.subscribe(function() {
    self.nextOpinionElements.removeClass('-ripple')
  });
};

OpinionModalView.prototype.hide = function () {
  this.cardsElements.removeClass('-inactive');
  this.cardsElements.addClass('-active');
};

OpinionModalView.prototype.show = function () {
  this.opinionModalElement.addClass('-show');
};

OpinionModalView.prototype.closeOpinionModal = function () {
  this.opinionModalElement.removeClass('-show');
};

OpinionModalView.prototype.showNextSuggestion = function() {
  var self = this;
  var first = self.modalContentElement.children('.-active').first();
  first.addClass('-next');
  first.find('.card').one('transitionend', function() {
    first.removeClass('-next');
    self.modalContentElement.append(first);

    events.showNextSuggestion.publish();
  });
};

OpinionModalView.prototype.opinionSent = function(opinion) {
  var self = this;
  var card = self.modalContentElement.children('.-active').first();
  card.addClass('-' + opinion);
  card.find('.card').one('transitionend', function() {
    card.remove();
    if (self.modalContentElement.children('.-active').length === 0) {
      
      self.closeOpinionModal();
      events.closeOpinionModal.publish();
    }

    events.showNextSuggestion.publish();
  });
};

OpinionModalView.prototype.activateOpinionCards = function(excerptId) {
  var self = this;
  if (excerptId) {
    self.cardsElements.removeClass('-active');
    self.cardsElements.addClass('-inactive');
    self.modalContentElement.find('[data-excerpt-id="' + excerptId + '"]')
      .addClass('-active')
      .removeClass('-inactive');
  }
};

OpinionModalView.prototype.hasActiveOpinionCards = function() {
  var self = this;
  return Boolean(self.cardsElements.length);
};

OpinionModalView.prototype.rippleCircleButton = function(circleButton) {
  circleButton.addClass('-ripple');
};
