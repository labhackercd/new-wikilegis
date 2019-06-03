/*global $ */

var DocumentOpinionsBodyView = function() {};

DocumentOpinionsBodyView.prototype.initEvents = function() {
  this.participantsButton = $('.js-participantsButton');
  this.opinionsButton = $('.js-opinionsButton');
  this.votesButton = $('.js-votesButton');
  this.publishers();
};

DocumentOpinionsBodyView.prototype.publishers = function () {
  var self = this;

  self.participantsButton.on('click', function() {
    $('.js-metricsButtons').children().removeClass('-active');
    self.participantsButton.addClass('-active');
    $('.js-documentExcerpt').removeClass('js-opinionsActive js-votesActive').addClass('js-participationActive');
  });

  self.opinionsButton.on('click', function() {
    $('.js-metricsButtons').children().removeClass('-active');
    self.opinionsButton.addClass('-active');
    $('.js-documentExcerpt').removeClass('js-participationActive js-votesActive').addClass('js-opinionsActive');
  });

  self.votesButton.on('click', function() {
    $('.js-metricsButtons').children().removeClass('-active');
    self.votesButton.addClass('-active');
    $('.js-documentExcerpt').removeClass('js-opinionsActive js-participationActive').addClass('js-votesActive');
  });
};