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
  this.submissionCues = $('.js-opinionModal .js-submissionCue');
  this.subscribers();
  this.publishers();
};

OpinionModalView.prototype.publishers = function() {
  var self = this;

  self.nextOpinionElements.click(function() {
    var buttonElement = $(this);
    var disabledButtons = buttonElement.siblings();

    self.rippleCircleButton(buttonElement);
    self.disableOpinionButtons(disabledButtons);

    events.nextOpinion.publish(
      buttonElement.data('opinion')
    );
  });

  self.buttonsElements.click(function() {
    var buttonElement = $(this);
    var disabledButtons = buttonElement.siblings();
    var cardElement = buttonElement.closest('.js-opinionCard');

    self.rippleCircleButton(buttonElement);
    self.disableOpinionButtons(disabledButtons);

    events.sendOpinion.publish(
      cardElement.data('suggestionId'),
      buttonElement.data('opinion')
    );
  });

};

OpinionModalView.prototype.subscribers = function () {
  var self = this;

  events.openOpinionModal.subscribe(function(excerptId){
    if(excerptId) {
      self.activateOpinionCards(excerptId);
    }
    if (self.modalContentElement.children('.-active').length > 0) {
      self.show();
    }
  });

  events.cancelTextSelection.subscribe(function() {
    self.hide();
  });

  events.nextOpinion.subscribe(function(opinion) {
    self.showNextSuggestion(opinion);
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

  events.showSubmissionCue.subscribe(function(opinion) {
    self.showSubmissionCue(opinion);
  });

  events.showNextSuggestion.subscribe(function() {
    self.unrippleCircleButton(self.nextOpinionElements);
    self.unrippleCircleButton(self.buttonsElements);
    self.enableOpinionButtons(self.nextOpinionElements);
    self.enableOpinionButtons(self.buttonsElements);
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

OpinionModalView.prototype.showNextSuggestion = function(opinion) {
  var self = this;
  var first = self.modalContentElement.children('.-active').first();
  first.addClass('-next');

  events.showSubmissionCue.publish(opinion);

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

  events.showSubmissionCue.publish(opinion);

  card.find('.card').on('transitionend', function(e) {
    if (e.originalEvent.propertyName === 'transform') {
      var excerptId = card.data('excerptId');

      card.remove();

      if($('.js-opinionModal .js-opinionCard').find('[data-excerpt-id="' + excerptId + '"]').length === 0) {
        events.hideExcerptOpinionBalloon.publish(excerptId);
      }
      if($('.js-opinionModal .js-opinionCard').length === 0) {
        events.hideDocumentOpinionBalloon.publish();
      }

      if (self.modalContentElement.children('.-active').length === 0) {
        self.closeOpinionModal();
        events.closeOpinionModal.publish();
      }
      $(this).off('transitionend');
      events.showNextSuggestion.publish();
    }
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

OpinionModalView.prototype.unrippleCircleButton = function(circleButton) {
  circleButton.removeClass('-ripple');
};

OpinionModalView.prototype.disableOpinionButtons = function(disabledButtons) {
  disabledButtons.addClass('-inactive');
};

OpinionModalView.prototype.enableOpinionButtons = function(disabledButtons) {
  disabledButtons.removeClass('-inactive');
};

OpinionModalView.prototype.showSubmissionCue = function(opinion) {
  var self = this;
  self.submissionCues.filter(`[data-opinion="${opinion}"]`).addClass('-show').one('animationend', function(){
    $(this).removeClass('-show');
  });
};
