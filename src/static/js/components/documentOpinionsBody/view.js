/*global $ */

var DocumentOpinionsBodyView = function() {};

DocumentOpinionsBodyView.prototype.initEvents = function() {
  this.participantsButton = $('.js-metricsButtons .js-participantsButton');
  this.opinionsButton = $('.js-metricsButtons .js-opinionsButton');
  this.votesButton = $('.js-metricsButtons .js-votesButton');
  this.publishers();
};

DocumentOpinionsBodyView.prototype.publishers = function () {
  var self = this;

  self.participantsButton.on('click', function() {
    $('.js-metricsButtons').children().removeClass('-active');
    self.participantsButton.addClass('-active');
    $('.js-documentExcerpt').removeClass('js-opinionsActive js-votesActive').addClass('js-participationActive');
    $('.js-metricsIcons').children().hide();
    $('.js-metricsIcons .js-participantsIcon').show();
  });

  self.opinionsButton.on('click', function() {
    $('.js-metricsButtons').children().removeClass('-active');
    self.opinionsButton.addClass('-active');
    $('.js-documentExcerpt').removeClass('js-participationActive js-votesActive').addClass('js-opinionsActive');
    $('.js-metricsIcons').children().hide();
    $('.js-metricsIcons .js-opinionsIcon').show();
  });

  self.votesButton.on('click', function() {
    $('.js-metricsButtons').children().removeClass('-active');
    self.votesButton.addClass('-active');
    $('.js-documentExcerpt').removeClass('js-opinionsActive js-participationActive').addClass('js-votesActive');
    $('.js-metricsIcons').children().hide();
    $(.'js-metricsIcons .js-votesIcon').show();
  });
};